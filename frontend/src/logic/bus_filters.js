import axios from "axios";

const USERS_PATH = "/users";
const BUS_FILTERS_PATH = "/bus_filters";
const TEMPLATE_PATH = "/templates";
const BUS_FILTERS_ENDPOINT = process.env.VUE_APP_NOTIFYME_HOST + BUS_FILTERS_PATH;

export default {
  get(busId) {
    return axios.get(BUS_FILTERS_ENDPOINT + "/" + busId);
  },
  getAll() {
    return axios.get(BUS_FILTERS_ENDPOINT);
  },
  post(busFilter) {
    return axios.post(BUS_FILTERS_ENDPOINT, busFilter);
  },
  put(busFilter) {
    return axios.put(BUS_FILTERS_ENDPOINT + "/" + busFilter.id, busFilter);
  },
  delete(busId) {
    return axios.delete(BUS_FILTERS_ENDPOINT + "/" + busId);
  },
  getSubscriptions(busId) {
    return axios.get(BUS_FILTERS_ENDPOINT + "/" + busId + USERS_PATH);
  },
  createSubscription(busId, users) {
    return axios.post(BUS_FILTERS_ENDPOINT + "/" + busId + USERS_PATH, users);
  },
  deleteSubscription(busId, userId) {
    return axios.delete(BUS_FILTERS_ENDPOINT + "/" + busId + USERS_PATH + "/" + userId)
  },
  getTemplate(busId) {
    return axios.get(BUS_FILTERS_ENDPOINT + "/" + busId + TEMPLATE_PATH)
  },
  createTemplate(busId, template) {
    return axios.post(BUS_FILTERS_ENDPOINT + "/" + busId + TEMPLATE_PATH, template)
  }
}
