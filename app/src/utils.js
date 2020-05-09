var isDebug = true;
var API_ROOT = isDebug ? "http://127.0.0.1:5000" : window.api_url;

export const formatURL = (relativePath) => {
  if (!relativePath.startsWith("/")) relativePath = "/" + relativePath;
  return API_ROOT + relativePath;
};

export default async function fetchAPI(relativePath) {
  return new Promise((resolve) => {
    fetch(formatURL(relativePath)).then((response) => {
      response.json().then((data) => {
        resolve(data);
      });
    });
  });
}
