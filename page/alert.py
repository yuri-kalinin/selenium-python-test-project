import data
import elem
from .pagebase import PageBase
from collections import namedtuple

class Alert(PageBase):

    def __init__(self, page):
        super().__init__(page)
        self.url = page.url + "/#!/alert"

        self.alert_search = elem.Text(page, model="search.alert")
        self.alert_add = elem.Button(page, click="addAlert()")
        self.alerts_table = elem.Table(page, repeat="alert in alerts track by $index")

        self.alert_save = elem.Button(page, click="saveAlert()")
        self.alert_name = elem.Text(page, model="alertDetail.name")
        self.alert_temperature_from = elem.Text(page, model="alertDetail.alert_from_f")
        self.alert_temperature_to = elem.Text(page, model="alertDetail.alert_to_f")
        self.alert_send_sms = elem.Checkbox(page, model="alertDetail.send_sms")
        self.alert_send_email = elem.Checkbox(page, model="alertDetail.send_email")
        self.alert_location_office_add = elem.Button(page, click="ensureAddOffice(officeItem)")
        self.alert_location_office_remove = elem.Button(page, click="removeOffice(office)")

    def open(self):
        self.alerts.wait_until_displayed()
        self.alerts.click()
        self.wait_loading_complete()

    def add_alert(self, alert: data.Alert):
        if self.alert_add.is_displayed():
            self.alert_add.click()
        self.alert_name.wait_until_displayed()
        self.alert_name.set_value(alert.name)
        self.alert_temperature_from.set_value(alert.temperature_from)
        self.alert_temperature_to.set_value(alert.temperature_to)
        self.alert_send_sms.set_value(alert.send_sms)
        self.alert_send_email.set_value(alert.send_email)
        if "Office" in alert.locations:
            self.alert_location_office_add.click()
            self.alert_location_office_remove.wait_until_displayed()
        self.alert_save.click()

    def edit_alert(self, alert: data.Alert):
        if alert.name is not None:
            self.alert_name.set_value(alert.name)
        if alert.temperature_from is not None:
            self.alert_temperature_from.set_value(alert.temperature_from)
        if alert.temperature_to is not None:
            self.alert_temperature_to.set_value(alert.temperature_to)
        if alert.send_sms is not None:
            self.alert_send_sms.set_value(alert.send_sms)
        if alert.send_email is not None:
            self.alert_send_email.set_value(alert.send_email)
        if "Office" in alert.locations:
            if self.alert_location_office_add.is_displayed():
                self.alert_location_office_add.click()
        else:
            if self.alert_location_office_remove.is_displayed():
                self.alert_location_office_remove.click()
        self.alert_save.wait_until_displayed()
        self.alert_save.click()

    def get_alerts(self):
        rows = self.alerts_table.get_data()
        Alert = namedtuple("Alert", ["id", "name", "temperature_from", "temperature_to", "send_sms", "send_email", "detect_potential_suspects"])
        alerts = [Alert(id=r[0], name=r[1], temperature_from=r[2], temperature_to=r[3], send_sms=r[4], send_email=r[5], detect_potential_suspects=r[6]) for r in rows]
        return alerts

    def search_alerts(self, value: str):
        self.alert_search.set_value(value)
        self.wait_loading_complete()
        self.alerts_table.wait_until_contains(value)
        return self.get_alerts()

    def open_alert_by_index(self, index: int):
        self.alerts_table.wait_until_displayed()
        self.alerts_table.find_all()[index].click()
        self.wait_loading_complete()
        self.alert_name.wait_until_displayed()

    def get_alert(self):
        alert = data.Alert(
            name=self.alert_name.get_value(),
            temperature_from=self.alert_temperature_from.get_value(),
            temperature_to=self.alert_temperature_to.get_value(),
            send_sms=self.alert_send_sms.get_value(),
            send_email=self.alert_send_email.get_value(),
            locations=[]
        )
        if self.alert_location_office_remove.is_displayed():
            alert.locations.append("Office")
        return alert