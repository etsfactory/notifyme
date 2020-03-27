import axios from "axios";

const USERS_PATH = "/users";
const BUS_FILTERS_PATH = "/bus_filters";
const USERS_ENDPOINT = process.env.VUE_APP_NOTIFYME_HOST + "/v1" + USERS_PATH;

export default {
  get(userId) {
    return axios.get(USERS_ENDPOINT + "/" + userId);
  },
  getAll() {
    return axios.get(USERS_ENDPOINT);
  },
  post(user) {
    return axios.post(USERS_ENDPOINT, user);
  },
  put(user) {
    return axios.put(USERS_ENDPOINT + "/" + user.id, user);
  },
  delete(userId) {
    return axios.delete(USERS_ENDPOINT + "/" + userId);
  },
  getSubscriptions(userId) {
    return axios.get(USERS_ENDPOINT + "/" + userId + BUS_FILTERS_PATH);
  },
  createSubscription(userId, busFilters) {
    return axios.post(
      USERS_ENDPOINT + "/" + userId + BUS_FILTERS_PATH,
      busFilters
    );
  },
  deleteSubscription(userId, busFilterId) {
    return axios.delete(
      USERS_ENDPOINT + "/" + userId + BUS_FILTERS_PATH + "/" + busFilterId
    );
  }
};
