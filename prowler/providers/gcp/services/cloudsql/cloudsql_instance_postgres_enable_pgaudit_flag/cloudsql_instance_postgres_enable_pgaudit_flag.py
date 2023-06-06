from prowler.lib.check.models import Check, Check_Report_GCP
from prowler.providers.gcp.services.cloudsql.cloudsql_client import cloudsql_client


class cloudsql_instance_postgres_enable_pgaudit_flag(Check):
    def execute(self) -> Check_Report_GCP:
        findings = []
        for instance in cloudsql_client.instances:
            if "POSTGRES" in instance.version:
                report = Check_Report_GCP(self.metadata())
                report.project_id = instance.project_id
                report.resource_id = instance.name
                report.resource_name = instance.name
                report.location = instance.region
                report.status = "FAIL"
                report.status_extended = f"PostgreSQL Instance {instance.name} has not 'cloudsql.enable_pgaudit' flag set to 'on'"
                for flag in instance.flags:
                    if (
                        flag["name"] == "cloudsql.enable_pgaudit"
                        and flag["value"] == "on"
                    ):
                        report.status = "PASS"
                        report.status_extended = f"PostgreSQL Instance {instance.name} has 'cloudsql.enable_pgaudit' flag set to 'on'"
                        break
                findings.append(report)

        return findings
