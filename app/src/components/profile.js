import React from "react";
import "../css/user-page.css";
import { getInitials, showTimestamp } from "../utils";

export function ProfilePicture(props) {
  let username = props.username;
  let initials = getInitials(username);
  return (
    <div className="profile-picture-wrapper">
      <div class="avatar-circle btn-outline-info img-fluid z-depth-1 rounded-circle view overlay">
        <span class="initials">{initials}</span>
        <a>
          <div class="mask rgba-white-slight"></div>
        </a>
      </div>
      <a>
        <div class="mask rgba-white-slight"></div>
      </a>
    </div>
  );
}

export default function UserProfile(props) {
  return (
    <div className="user-profile">
      <div className="user-profile-header">
        <ProfilePicture username={props.username} />
        <br />
        <br />
      </div>
      <div className="user-profile-details">
        <h4>
          <b>Name:</b> {props.username}
        </h4>
        <br />
        <h4>
          <b>User ID :</b>
          {props.userId}
        </h4>
        <br />
        <h4>
          <b>Birthday: </b>
          {showTimestamp(props.birthday)}
        </h4>
        <br />
        <h4>
          <b>Gender: </b>
          {props.gender[0]}
        </h4>
      </div>
    </div>
  );
}
