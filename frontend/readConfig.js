const fs = require("fs");
const ConfigParser = require("configparser");

const readConfig = () => {
  const exists = fs.existsSync(process.env.CONFIG_FILE_PATH);
  if (exists) {
    const env = {};
    const config = new ConfigParser();
    config.read(process.env.CONFIG_FILE_PATH);

    const setEnvParam = (section, iniParam, envParam) => {
      const value = config.get(section, iniParam);
      if (value) env[envParam] = `"${value}"`;
    };

    setEnvParam("APIS", "notifyme_host", "VUE_APP_NOTIFYME_HOST");

    return {
      "process.env": env
    };
  }
};

module.exports = readConfig;
