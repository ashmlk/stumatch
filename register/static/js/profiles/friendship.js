$(document).ready(function (){

    var friendShipLoading = `<div class="d-flex w-100 align-items-center justify-content-center">
    <div class="px-2">
      <div class="spinner-border spinner-border-sm text-muted-jc" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
    <div class="d-flex align-items-center">
      <div class="font-auto-sm text-muted-jc">
        Loading
      </div>
    </div>
  </div>`;
    var friendShipStatusReceivedError = `<div class="d-flex w-100 align-items-center justify-content-center">
    <div class="d-flex w-100 border rounded align-items-center">
      <div class="font-auto-sm text-muted-jc">
        Error
      </div>
    </div>
  </div>`;

    $.initialize('.friendship-container', function(){
        let otherUserId = $(this).attr('data-uid')
        getFriendShipStatus(id=otherUserId, container=$(this));
    })

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          var cookies = document.cookie.split(";");
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
    
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    var csrftoken = getCookie("csrftoken");
    
    $.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    });

    function friendshipButtonCreator(url, label, btnStyle){
        let btn = `<div class="friendship-action-ctr d-flex w-100 align-items-center px-2" >
                        <div class="friendship-action-link w-100">
                            <button type="button" data-url="${url}" class="no-outline w-100 friendship-action-btn btn btn-sm ${btnStyle}">
                                <span>
                                    ${label}
                                </span>
                            </button>
                        </div>
                    </div>`
        return btn;
    }

    function getEditProfileContainer(id){
        let btn = `<div class="friendship-action-ctr d-flex w-100 align-items-center px-2" >
                        <div class="friendship-action-link w-100">
                            <a href="/settings/edit/profile/" class="no-outline w-100 no-underline btn btn-sm btn-default border text-dark rounded">
                                <span>
                                    Edit Profile
                                </span>
                            </a>
                        </div>
                    </div>`
        return btn;
        
    }
    function getPendingFriendshipRequest(id){
        let url = `/friends/request/${id}/action/remove-pending/`
        let pendingRequestButtonContainer = friendshipButtonCreator(url, "Pending", "btn-default border text-dark bg-white");
        return pendingRequestButtonContainer;
    }

    function getAcceptDeleteFriendshipRequest(id){
        let urlForDelete = `/friends/request/${id}/action/delete-request/`;
        let urlForAccept = `/friends/request/${id}/action/accept-request/`;
        let acceptFriendRequestButtonContainer = friendshipButtonCreator(urlForAccept, "Accept", "btn-primary");
        let deleteFriendRequestButtonContainer = friendshipButtonCreator(urlForDelete, "Delete", "btn-default border text-dark bg-white");
        let acceptRejectButtons = `<div class="d-flex align-items-center w-100">
                                    ${acceptFriendRequestButtonContainer} ${deleteFriendRequestButtonContainer} 
                                </div>`
        return acceptRejectButtons;
    }
    
    function getRemoveFriendship(id){
        let url = `/friends/${id}/remove/`;
        let removeFriendshipButtonContainer = friendshipButtonCreator(url, 'Remove', "btn-default border bg-white text-dark");
        return removeFriendshipButtonContainer;
    }

    function getAddUser(id){
        let url = `/friends/${id}/add/`;
        let addFriendButtonContainer = friendshipButtonCreator(url, 'Add', "btn-primary");
        return addFriendButtonContainer;
    }

    function getUnblockUser(id){
        let url  = `/users/unblock/${id}/`
        let unblockUserButtonContainer = friendshipButtonCreator(url, 'Unblock', 'btn-default border text-dark bg-white');
        return unblockUserButtonContainer;
    }

    function getFriendShipStatus(id, container){
        $.ajax({
            url:`/friendship/status/${id}/`,
            type: "get",
            dataType: "json",
            beforeSend: function () {
              $(container).find('.friendship-status-ctr').html(friendShipLoading);
            },
            success: function (data) {
                $(container).find('.friendship-loading-ctr').remove();
                let actionContainerFunctions = {
                    "viewer_sent_friend_request": getPendingFriendshipRequest,
                    "viewer_received_friend_request": getAcceptDeleteFriendshipRequest,
                    "viewer_is_friend": getRemoveFriendship,
                    "viewer_has_blocked": getUnblockUser,
                    "viewer_has_no_relation":getAddUser,
                    "viewer_is_user":getEditProfileContainer,
                }
                let otherUserID = data['other_user_id'];
                let statusReturned = Object.keys(data['status']).filter(k => data['status'][k]); // get the value which is true AKA - the status
                let actionContainer = actionContainerFunctions[statusReturned](otherUserID);
                $(container).append(actionContainer);
            },
        })
    }

    $(document).on('click', '.friendship-action-link .friendship-action-btn', function (){
        let friendShipActionButton  =$(this);
        $.ajax({
            url: $(friendShipActionButton).attr("data-url"),
            type: "POST",
            data: {
                csrfmiddlewaretoken: getCookie("csrftoken")
            },
            dataType: "json",
            success: function (data) {
                let otherUserID = data['other_user_id'];
                let friendshipContainer = $(friendShipActionButton).closest('.friendship-container');
                $(friendshipContainer).empty();
                getFriendShipStatus(id=otherUserID, container=friendshipContainer);
            },
          });
    })

})