import React, { useState, useEffect } from "react";
import "../css/user-page.css";
import { fetchAPI, showTimestamp } from "../utils";

function Snapshot(props) {
  let userId = props.userId;
  let username = props.username;
  let snapshotId = props.snapshotId;
  let datetime = showTimestamp(props.datetime);

  let [results, setDetails] = useState({ results: [] });
  useEffect(() => {
    fetchAPI(`/users/${userId}/snapshots/${snapshotId}`).then((data) => {
      setDetails({ results: data.results });
    });
  }, []);

  return (
    <div className="snapshot-container">
      <div className="jumbotron text-center hoverable p-4 snapshot">
        <div class="row">
          <div class="col-md-4 offset-md-1 mx-3 my-3">
            <div class="view overlay">
              <img
                src="https://mdbootstrap.com/img/Photos/Others/laptop-sm.jpg"
                class="img-fluid"
                alt="Sample image for first version of blog listing"
              />
              <a>
                <div class="mask rgba-white-slight"></div>
              </a>
            </div>
          </div>

          <div class="col-md-7 text-md-left ml-3 mt-3">
            <h4 class="h4 mb-4">Snapshot #{snapshotId}</h4>

            <p class="font-weight-normal">
              by{" "}
              <a>
                <strong>{username}</strong>
              </a>
              , {datetime}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function UserSnapshots(props) {
  let userId = props.userId;
  let [snapshots, setSnapshots] = useState([]);

  useEffect(() => {
    fetchAPI(`/users/${userId}/snapshots`).then((data) => {
      setSnapshots(data);
    });
  }, []);

  let snapshotViews = [];
  snapshots.forEach((snapshot) => {
    snapshotViews.push(
      <Snapshot
        userId={userId}
        username={props.username}
        snapshotId={snapshot.uuid}
        datetime={snapshot.datetime}
      />
    );
  });

  return <div className="user-snapshots">{snapshotViews}</div>;
}

export default UserSnapshots;
