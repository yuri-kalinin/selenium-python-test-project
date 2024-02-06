import data
import page
import test

class TestSearch(test.TestBase):

    @test.fixture(scope="class", autouse=True)
    def page_alert(self):
        page_login = page.Login(self)
        page_login.open()
        assert page_login.is_opened()

        page_login.login(self.config['username'], self.config['password'])
        page_alert = page.Alert(self)
        return page_alert

    def test_valid_data_alert_add(self, page_alert: page.Alert):
        alert = data.Alert(name=data.Input.get_time_str("name"), temperature_from="24", temperature_to="42", send_sms=True, send_email=True, locations=["Office"])

        page_alert.open()
        page_alert.add_alert(alert)
        alerts = page_alert.search_alerts(alert.name)

        assert len(alerts) == 1 and alerts[0].name == alert.name

    def test_valid_data_alert_edit(self, page_alert: page.Alert):
        page_alert.open()
        page_alert.open_alert_by_index(0)
        alertOld = page_alert.get_alert()
        alertNew = data.Alert(
            name=data.Input.get_time_str("name"),
            temperature_from="24" if alertOld.temperature_from != "24" else "25",
            temperature_to="42" if alertOld.temperature_to != "42" else "43",
            send_sms=not alertOld.send_sms,
            send_email=not alertOld.send_email,
            locations=["Office"] #TODO: for now this is the only available valid option
        )

        page_alert.edit_alert(alertNew)
        alertsOld = page_alert.search_alerts(alertOld.name)
        alertsNew = page_alert.search_alerts(alertNew.name)
        page_alert.open_alert_by_index(0)
        alert = page_alert.get_alert()

        assert len(alertsOld) == 0 and len(alertsNew) == 1 and alert == alertNew

    def test_invalid_data_alert_add_fails(self, page_alert: page.Alert):
        alert = data.Alert(name=data.Input.get_time_str("name"), temperature_from="twenty", temperature_to="forty", send_sms=True, send_email=True, locations=["Office"])

        page_alert.open()
        page_alert.add_alert(alert)

        errors = page_alert.wait_errors()
        alerts = page_alert.search_alerts(alert.name)

        assert len(alerts) == 0 and len(errors) == 2 and errors[0] == "Alert From is required." and errors[1] == "Alert to is required."