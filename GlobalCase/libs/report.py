import os
from datetime import datetime

class Report:
    def __init__(self, name="report"):
        self.results = []
        self.start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S").replace(":", "-")
        self.report_filename = f"{name}_{self.start_time}.txt"
        self.ui_url = None
        self.ems_version = None
        self.node_name = None
        self.node_ip = None
        self.node_chassis = None

    def set_environment(self, ui_url, ems_version, node_name, node_ip, node_chassis):
        self.ui_url = ui_url
        self.ems_version = ems_version
        self.node_name = node_name
        self.node_ip = node_ip
        self.node_chassis = node_chassis

    def log_result(self, test_case_id, test_name, test_status):
        self.results.append({
            "test_case_id": test_case_id,
            "test_name": test_name,
            "test_status": test_status,
        })

    def write_report(self):
        report_data = [
            f"Report generated on: {self.start_time}",
            f"UI URL: {self.ui_url}",
            f"EMS Version: {self.ems_version}",
            f"Node Name: {self.node_name}",
            f"Node IP: {self.node_ip}",
            f"Node Chassis: {self.node_chassis}",
            "",
            "Test Results:",
            "-------------"
        ]
        for result in self.results:
            report_data.append(
                f"[{result['test_case_id']}][{result['test_name']}] Result {result['test_status']}"
            )

        report_path = os.path.join("reports", self.report_filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_data))

        print(f"Report written to {report_path}")
