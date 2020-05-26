var isDebug = true;
var API_ROOT = isDebug ? "http://127.0.0.1:5000" : window.api_url;

export const showTimestamp = (datetime) => {
  let date = new Date(parseInt(datetime));
  return date.toLocaleString().slice(0, -3);
};

export const formatURL = (relativePath) => {
  if (!relativePath.startsWith("/")) relativePath = "/" + relativePath;
  return API_ROOT + relativePath;
};

export async function fetchAPI(relativePath) {
  return new Promise((resolve) => {
    fetch(formatURL(relativePath)).then((response) => {
      response.json().then((data) => {
        resolve(data);
      });
    });
  });
}

export const getInitials = (name) => {
  let firstLastName = name.split(" ");
  if (firstLastName.length < 2) return name[0];
  let initials = firstLastName[0][0] + firstLastName[1][0];
  return initials;
};
