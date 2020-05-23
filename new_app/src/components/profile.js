import React, { useEffect, useState } from "react";
import "../css/user-page.css";
import { fetchAPI, getInitials, showTimestamp } from "../utils";

export default function UserProfile(props) {
  return (
    <div className="user-profile">
      <div className="user-profile-header">
        <h1>{props.username}</h1>
      </div>
      <div className="user-profile-details">
        <h4>
          <b>User ID :</b>
          {props.userId}
        </h4>
        <h4>
          <b>Birthday: </b>
          {showTimestamp(props.birthday)}
        </h4>
        <h4>
          <b>Gender: </b>
          {props.gender[0]}
        </h4>
      </div>
    </div>
  );
}
