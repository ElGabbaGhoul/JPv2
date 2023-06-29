## 6/23
 - created playlist API

## 6/24
 - created accounts API
 - working on adding user authentication -- https://www.youtube.com/watch?v=5GxQ1rLTwaU 

## 6/26
 - finished adding user authentication (including validation)
 - Playlist API -- check CRUD functionality of all playlist APIs. Update so that only user that creates playlist can see that playlist.
   - Checked APIs, all function as intended. Working on Account APIs. 
 - Accounts API -- create CRUD functionality for Account APIs, factored so that you need an account to create a playlist.
   - Created create_new_user api, functioning as intended. 

## 6/28
 - created frontend folder with flowbite-svelte

## 6/29
  TODOS FOR TODAY:
  - create login page
  - finish crud functions for account backend
  - sync the two so I can create a user on frontend
  
  Blockers:
  - Create New User
    - Failed to fetch. Reason: cors, network failure, or url scheme
  - get all users
    - validation errors when trying to create user object - FIXED
    - Failed to fetch. Reason: cors, network failure, or url scheme
  - Create new playlist
    - 422 unprocessable entity when trying to create new playlist object - FIXED
    - Create new playlist working as intended
  - Fetch all playlists
    - 500 internal server error - 5 validation errors. created_by, track dictionary