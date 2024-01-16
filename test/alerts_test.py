import data
import page
import test

class TestSearch(test.TestBase):

    @test.fixture(scope="class", autouse=True)
    def setup(self):
        self.page = page.Login(self)
        self.page.open()
        assert self.page.is_opened()

        self.page.login(self.config['username'], self.config['password'])
        return self

    def test_valid_data_alert_add(self, setup):
        alert = data.Alert(name=data.Input.get_time_str("name"), temperature_from="24", temperature_to="42", send_sms=True, send_email=True, locations=["Office"])

        self.page = page.Alert(setup)
        self.page.open()
        self.page.add_alert(alert)
        self.page.search_alerts(alert.name)
        alerts = self.page.get_alerts()

        assert len(alerts) == 1, alerts[0].name == alert.name

    def test_valid_data_alert_edit(self, setup):
        self.page = page.Alert(setup)
        self.page.open()
        self.page.open_alert_by_index(0)
        alertOld = self.page.get_alert()
        alertNew = data.Alert(
            name=data.Input.get_time_str("name"),
            temperature_from="24" if alertOld.temperature_from != "24" else "25",
            temperature_to="42" if alertOld.temperature_to != "42" else "43",
            send_sms=not alertOld.send_sms,
            send_email=not alertOld.send_email,
            locations=["Office"] #TODO: for now this is the only available valid option
        )

        self.page.edit_alert(alertNew)
        alertsOld = self.page.search_alerts(alertOld.name)
        alertsNew = self.page.search_alerts(alertNew.name)
        self.page.open_alert_by_index(0)
        alert = self.page.get_alert()

        assert (len(alertsOld) == 0, len(alertsNew) == 1, alert == alertNew)

    def test_invalid_data_alert_add_fails(self, setup):
        alert = data.Alert(name=data.Input.get_time_str("name"), temperature_from="twenty", temperature_to="forty", send_sms=True, send_email=True, locations=["Office"])

        self.page = page.Alert(setup)
        self.page.open()
        self.page.add_alert(alert)

        errors = self.page.wait_errors()
        alerts = self.page.search_alerts(alert.name)

        assert (len(alerts) == 0, len(errors) == 2, errors[0] == "Alert From is required.", errors[1] == "Alert to is required.")