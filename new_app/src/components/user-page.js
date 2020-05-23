import React, { useEffect, useState } from "react";
import "../css/user-page.css";
import { fetchAPI } from "../utils";
import UserProfile from "./profile";
import UserSnapshots from "./snapshots";

function UserPage(props) {
  let match = props.match;
  let userId = match.params.id;

  let [details, setDetails] = useState({
    username: "",
    birthday: 0,
    gender: "",
  });

  useEffect(() => {
    fetchAPI(`/users/${userId}`).then((data) => {
      setDetails({
        username: data.username,
        birthday: data.birthday,
        gender: data.gender,
      });
    });
  }, []);

  return (
    <div className="user-page">
      <UserProfile
        userId={userId}
        username={details.username}
        birthday={details.birthday}
        gender={details.gender}
      />
      <UserSnapshots userId={userId} username={details.username} />
    </div>
  );
}

export default UserPage;
