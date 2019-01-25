import axios from "axios";

const TEMPLATES_PATH = "/templates";
const TEMPLATES_ENDPOINT = process.env.VUE_APP_NOTIFYME_HOST + TEMPLATES_PATH;

export default {
  get(templateId) {
    return axios.get(TEMPLATES_ENDPOINT + "/" + templateId);
  },
  getAll() {
    return axios.get(TEMPLATES_ENDPOINT);
  },
  post(template) {
    return axios.post(TEMPLATES_ENDPOINT, template);
  },
  put(template) {
    return axios.put(TEMPLATES_ENDPOINT + "/" + template.id, template);
  },
  delete(templateId) {
    return axios.delete(TEMPLATES_ENDPOINT + "/" + templateId);
  }
};
