import axios from "axios";

const MESSAGES_PATH = "/messages";
const MESSAGES_ENDPOINT = process.env.VUE_APP_NOTIFYME_HOST + MESSAGES_PATH;

export default {
  getAll() {
    return axios.get(MESSAGES_ENDPOINT);
  }
};
