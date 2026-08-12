from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ZEALMAN_SCRIPTS = REPO_ROOT / "skills" / "use-zealman-autodl-workflows" / "scripts"
PROMPT_SCRIPTS = REPO_ROOT / "skills" / "write-game-video-prompt" / "scripts"
DECISION_LOG_SCHEMA = (
    REPO_ROOT / "skills" / "write-game-video-prompt" / "assets" / "decision-log.schema.json"
)

STAGED_WORKFLOW = {
    "_api_config": {
        "customLabels": {
            "5:text": "提示词",
            "7:image": "首帧",
            "9:seed": "随机种子",
            "11:Number": "时长",
        },
        "enabledParams": {
            "5:text": True,
            "7:image": True,
            "9:seed": True,
            "11:Number": True,
            "12:width": False,
        },
        "formValues": {},
    },
    "5": {"class_type": "Text Multiline", "inputs": {"text": "default"}},
    "7": {"class_type": "LoadImage", "inputs": {"image": "default.png"}},
    "9": {"class_type": "easy seed", "inputs": {"seed": 0}},
    "11": {"class_type": "Int", "inputs": {"Number": "5"}},
    "12": {"class_type": "Size", "inputs": {"width": 512}},
}


def run_script(
    script: Path, *args: object, expect_success: bool = True
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(script), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_success and completed.returncode != 0:
        raise AssertionError(
            f"{script.name} failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def make_job(directory: Path, execution: str = "local", upload_approved: bool = False) -> Path:
    (directory / "anchor.png").write_bytes(b"\x89PNG-fake-anchor")
    prompts = directory / "prompts"
    prompts.mkdir(exist_ok=True)
    (prompts / "final.txt").write_text("A neon drink billboard loop.\n", encoding="utf-8")
    job = {
        "schema_version": "0.1.0",
        "job_id": "neon-billboard-loop-001",
        "workflow": "in-game-loop",
        "goal": "Loopable billboard advertisement.",
        "inputs": {
            "assets": [
                {
                    "id": "loop-first",
                    "type": "image",
                    "source": "anchor.png",
                    "role": "First frame anchor.",
                    "rights_status": "owned",
                    "remote_upload_approved": upload_approved,
                }
            ]
        },
        "generation": {
            "provider": "zealman-autodl",
            "model": "wan-2.2-flf",
            "mode": "first-last-frame-to-video",
            "duration_seconds": 8,
            "aspect_ratio": "16:9",
            "resolution": "1280x720",
            "audio": False,
            "variants": 2,
            "execution": execution,
            "provider_terms_approved": True,
            "paid_generation": False,
            "paid_generation_approved": False,
        },
        "delivery": {"kind": "video-texture", "loop": True, "fps": 24, "containers": ["mp4"]},
        "rights": {
            "public_release": False,
            "ai_disclosure_decision": "pending",
            "notes": "Internal test.",
        },
        "qa_checks": ["continuity", "text", "seam"],
    }
    job_path = directory / "game-video-job.json"
    job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
    return job_path


def stage_test_workflow(directory: Path) -> Path:
    staged = directory / "lumio-test.json"
    staged.write_text(json.dumps(STAGED_WORKFLOW, ensure_ascii=False, indent=2), encoding="utf-8")
    sidecar = directory / "lumio-test.json.source.json"
    sidecar.write_text(
        json.dumps({"schema_version": 1, "status": "staged"}, indent=2), encoding="utf-8"
    )
    return staged


def build_run_request(workdir: Path, execution: str = "local", upload_approved: bool = False) -> Path:
    job_path = make_job(workdir, execution=execution, upload_approved=upload_approved)
    staged = stage_test_workflow(workdir)
    request_path = workdir / "run-request.json"
    run_script(
        ZEALMAN_SCRIPTS / "apply_job.py",
        staged,
        "--job",
        job_path,
        "--map",
        "5:text=prompt:prompts/final.txt",
        "--map",
        "7:image=asset:loop-first",
        "--map",
        "9:seed=seed:42",
        "--map",
        "11:Number=job:generation.duration_seconds",
        "--output",
        request_path,
    )
    return request_path


class MockPanelHandler(BaseHTTPRequestHandler):
    state: dict[str, object] = {}

    def log_message(self, *args: object) -> None:
        pass

    def _send_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        state = type(self).state
        if self.path == "/api/health":
            self._send_json({"success": True, "status": "ok"})
        elif self.path == "/api/workflow/list":
            self._send_json({"workflows": state.setdefault("saved", [])})
        elif self.path.startswith("/api/workflow/result"):
            prompt_id = self.path.split("prompt_id=")[-1]
            polls: dict[str, int] = state.setdefault("polls", {})  # type: ignore[assignment]
            polls[prompt_id] = polls.get(prompt_id, 0) + 1
            if polls[prompt_id] == 1:
                self._send_json({"success": True, "pending": True, "results": []})
            else:
                self._send_json(
                    {
                        "success": True,
                        "pending": False,
                        "prompt_id": prompt_id,
                        "results": [
                            {
                                "type": "video",
                                "url": f"/output/test/{prompt_id}.mp4",
                                "filename": f"{prompt_id}.mp4",
                            }
                        ],
                    }
                )
        elif self.path.startswith("/output/"):
            body = f"video-bytes-{self.path}".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        state = type(self).state
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        if self.path == "/api/comfy/upload/file":
            uploads: list[int] = state.setdefault("uploads", [])  # type: ignore[assignment]
            uploads.append(len(raw))
            self._send_json({"name": "uploaded-anchor.png", "subfolder": "", "type": "input"})
        elif self.path == "/api/workflow/save":
            payload = json.loads(raw.decode("utf-8"))
            saved: list[dict[str, object]] = state.setdefault("saved", [])  # type: ignore[assignment]
            saved.append({"id": payload["workflow_id"]})
            state["save_payload"] = payload
            self._send_json({"success": True})
        elif self.path == "/api/workflow/generate":
            payload = json.loads(raw.decode("utf-8"))
            submissions: list[dict[str, object]] = state.setdefault("submissions", [])  # type: ignore[assignment]
            submissions.append(payload)
            self._send_json({"success": True, "prompt_id": f"p-{len(submissions)}"})
        else:
            self._send_json({"error": "not found"}, status=404)


class ApplyJobTests(unittest.TestCase):
    def test_builds_run_request_from_job_and_staged_workflow(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-apply-") as temp:
            workdir = Path(temp)
            request_path = build_run_request(workdir)
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["kind"], "zealman-run-request")
            self.assertEqual(request["job_id"], "neon-billboard-loop-001")
            self.assertEqual(request["workflow_id"], "lumio-test.json")
            self.assertEqual(request["execution"], "local")
            self.assertEqual(request["variants"], 2)
            self.assertEqual(request["seed_param"], "9:seed")
            self.assertEqual(
                request["input_values"]["5:text"], "A neon drink billboard loop."
            )
            self.assertEqual(request["input_values"]["9:seed"], 42)
            self.assertEqual(request["input_values"]["11:Number"], 8)
            file_input = request["file_inputs"]["7:image"]
            self.assertTrue(file_input["path"].endswith("anchor.png"))
            self.assertEqual(file_input["asset_id"], "loop-first")
            self.assertFalse(file_input["remote_upload_approved"])

    def test_rejects_disabled_and_unknown_parameters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-apply-") as temp:
            workdir = Path(temp)
            job_path = make_job(workdir)
            staged = stage_test_workflow(workdir)
            disabled = run_script(
                ZEALMAN_SCRIPTS / "apply_job.py",
                staged,
                "--job",
                job_path,
                "--map",
                "12:width=int:768",
                expect_success=False,
            )
            self.assertIn("not in enabledParams", disabled.stderr)
            unknown = run_script(
                ZEALMAN_SCRIPTS / "apply_job.py",
                staged,
                "--job",
                job_path,
                "--map",
                "99:text=text:hello",
                "--allow-disabled",
                expect_success=False,
            )
            self.assertIn("does not exist in the staged workflow", unknown.stderr)

    def test_list_shows_enabled_parameters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-apply-") as temp:
            staged = stage_test_workflow(Path(temp))
            completed = run_script(ZEALMAN_SCRIPTS / "apply_job.py", staged, "--list")
            self.assertIn("5:text", completed.stdout)
            self.assertIn("[file]", completed.stdout)


class RunWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        MockPanelHandler.state = {}
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MockPanelHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_end_to_end_run_registers_uploads_generates_and_downloads(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-run-") as temp:
            workdir = Path(temp)
            request_path = build_run_request(workdir)
            output_dir = workdir / "candidates"
            completed = run_script(
                ZEALMAN_SCRIPTS / "run_workflow.py",
                request_path,
                "--output-dir",
                output_dir,
                "--base-url",
                self.base_url,
                "--poll-interval",
                "0.05",
                "--register",
            )
            self.assertIn('"status": "rendered"', completed.stdout)

            state = MockPanelHandler.state
            self.assertEqual(len(state["uploads"]), 1)
            self.assertEqual(state["save_payload"]["workflow_id"], "lumio-test.json")
            submissions = state["submissions"]
            self.assertEqual(len(submissions), 2)
            for submission in submissions:
                self.assertEqual(submission["workflow_id"], "lumio-test.json")
                self.assertEqual(submission["input_values"]["7:image"], "uploaded-anchor.png")
            self.assertEqual(submissions[0]["input_values"]["9:seed"], 42)
            self.assertNotEqual(submissions[1]["input_values"]["9:seed"], 42)

            self.assertTrue((output_dir / "c-001" / "p-1.mp4").is_file())
            self.assertTrue((output_dir / "c-002" / "p-2.mp4").is_file())

            log = json.loads((output_dir / "decision-log.json").read_text(encoding="utf-8"))
            self.assertEqual(log["job_id"], "neon-billboard-loop-001")
            self.assertEqual(len(log["candidates"]), 2)
            schema = json.loads(DECISION_LOG_SCHEMA.read_text(encoding="utf-8"))
            required = set(schema["$defs"]["candidate"]["required"])
            allowed = set(schema["$defs"]["candidate"]["properties"])
            for candidate in log["candidates"]:
                self.assertEqual(candidate["status"], "generated")
                self.assertFalse(required - set(candidate))
                self.assertFalse(set(candidate) - allowed)
                self.assertEqual(len(candidate["outputs"]), 1)

            sidecar = json.loads(
                (workdir / "lumio-test.json.source.json").read_text(encoding="utf-8")
            )
            self.assertEqual(sidecar["status"], "rendered")
            self.assertEqual(sidecar["runs"][0]["candidate_ids"], ["c-001", "c-002"])
            self.assertNotIn(self.base_url, json.dumps(sidecar))

    def test_refuses_plan_only_and_unapproved_remote_uploads(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-run-") as temp:
            workdir = Path(temp) / "plan-only"
            workdir.mkdir()
            request_path = build_run_request(workdir, execution="plan-only")
            completed = run_script(
                ZEALMAN_SCRIPTS / "run_workflow.py",
                request_path,
                "--output-dir",
                workdir / "candidates",
                expect_success=False,
            )
            self.assertIn("plan-only", completed.stderr)

            remote_dir = Path(temp) / "remote"
            remote_dir.mkdir()
            remote_request = build_run_request(remote_dir, execution="remote", upload_approved=False)
            refused = run_script(
                ZEALMAN_SCRIPTS / "run_workflow.py",
                remote_request,
                "--output-dir",
                remote_dir / "candidates",
                expect_success=False,
            )
            self.assertIn("remote_upload_approved", refused.stderr)
            self.assertIn("loop-first", refused.stderr)

    def test_dry_run_makes_no_network_calls(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-run-") as temp:
            workdir = Path(temp)
            request_path = build_run_request(workdir)
            completed = run_script(
                ZEALMAN_SCRIPTS / "run_workflow.py",
                request_path,
                "--output-dir",
                workdir / "candidates",
                "--dry-run",
            )
            plan = json.loads(completed.stdout)
            self.assertEqual(plan["workflow_id"], "lumio-test.json")
            self.assertEqual(plan["variants"], 2)
            self.assertEqual(MockPanelHandler.state, {})


class LogCandidateTests(unittest.TestCase):
    def test_full_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lumio-log-") as temp:
            workdir = Path(temp)
            job_path = make_job(workdir)
            log_path = workdir / "decision-log.json"
            script = PROMPT_SCRIPTS / "log_candidate.py"

            run_script(script, "init", "--job", job_path, "--log", log_path)
            repeated = run_script(
                script, "init", "--job", job_path, "--log", log_path, expect_success=False
            )
            self.assertIn("refusing to overwrite", repeated.stderr)

            output_file = workdir / "clip.mp4"
            output_file.write_bytes(b"clip-bytes")
            run_script(
                script,
                "add",
                "--log",
                log_path,
                "--candidate-id",
                "c-001",
                "--adapter",
                "zealman-autodl",
                "--seed",
                "42",
                "--workflow-id",
                "lumio-test.json",
                "--output",
                output_file,
            )
            run_script(
                script,
                "add",
                "--log",
                log_path,
                "--candidate-id",
                "c-002",
                "--adapter",
                "zealman-autodl",
                "--status",
                "failed",
                "--note",
                "panel error",
            )
            run_script(
                script,
                "reject",
                "--log",
                log_path,
                "--candidate-id",
                "c-001",
                "--reason",
                "seam visible at loop point",
            )
            blocked = run_script(
                script,
                "select",
                "--log",
                log_path,
                "--candidate-id",
                "c-001",
                expect_success=False,
            )
            self.assertIn("only a generated candidate", blocked.stderr)

            log = json.loads(
                run_script(script, "show", "--log", log_path, "--json").stdout
            )
            self.assertEqual(log["job_id"], "neon-billboard-loop-001")
            statuses = {c["candidate_id"]: c["status"] for c in log["candidates"]}
            self.assertEqual(statuses, {"c-001": "rejected", "c-002": "failed"})
            self.assertEqual(
                log["candidates"][0]["rejection_reason"], "seam visible at loop point"
            )
            self.assertEqual(len(log["candidates"][0]["outputs"]), 1)
            self.assertEqual(log["candidates"][0]["outputs"][0]["type"], "video")

    def test_decision_log_schema_is_valid_json(self) -> None:
        schema = json.loads(DECISION_LOG_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$defs"]["candidate"]["properties"]["status"]["enum"],
                         ["generated", "failed", "rejected", "selected"])


if __name__ == "__main__":
    unittest.main()
