import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../css/users-page.css";
import { ProfilePicture } from "../components/profile";
import { fetchAPI, showTimestamp, getInitials } from "../utils";

function UserEntry(props) {
  let userId = props.userId;
  let username = props.username;
  let [details, setDetails] = useState({ birthday: 0, gender: "" });
  useEffect(() => {
    fetchAPI(`/users/${userId}`).then((data) => {
      setDetails({ birthday: data.birthday, gender: data.gender });
    });
  }, []);
  return (
    <section class="dark-grey-text hoverable user-entry">
      <div class="row align-items-center">
        <div class="col-lg-5 col-xl-4">
          <Link to={`/users/${userId}`}>
            <div className="profile-picture-link">
              <ProfilePicture username={username} />
            </div>
          </Link>
        </div>
        <div class="col-lg-7 col-xl-8 user-details-text">
          <h4 class="font-weight-bold mb-3">
            <strong>{username}</strong>
          </h4>
          <p class="">
            <b>User ID: </b>
            {userId} <br />
            <b>Username: </b>
            {username} <br />
            <b>Birthday: </b>
            {showTimestamp(details.birthday)} <br />
            <b>Gender: </b>
            {details.gender}
          </p>
          <Link to={`/users/${userId}`}>
            <button
              type="button"
              class="btn aqua-gradient waves-effect show-snapshots-btn"
            >
              Show snapshots
            </button>
          </Link>
        </div>
      </div>

      <hr class="my-5 white" />
    </section>
  );
}

function UsersPage() {
  var [usersList, setUsersList] = useState([]);
  useEffect(() => {
    fetchAPI("/users").then((data) => {
      setUsersList(data);
    });
  }, []);

  let users = [];
  usersList.forEach((user) => {
    users.push(<UserEntry userId={user.user_id} username={user.username} />);
  });

  return (
    <div className="users-page">
      <div class="container mt-5 users-list-container">{users}</div>
    </div>
  );
}

export default UsersPage;
