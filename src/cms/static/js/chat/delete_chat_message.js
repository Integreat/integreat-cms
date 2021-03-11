/**
 * This file contains the deletion function for the author chat
 */

// Listen on the custom event "action-confirmed" which is triggered by the confirmation popup
u('.confirmation-button').handle('action-confirmed', delete_chat_message);

// Function to delete a chat message
async function delete_chat_message(event) {
    // Hide error in case it was shown before
    u('#chat-network-error').addClass("hidden");
    u('#chat-server-error').addClass("hidden");

    // Delete chat message
    let deletion_button = u(event.target).closest(".confirmation-button")
    fetch(deletion_button.data("action"), {
        method: 'POST',
        headers: {
            "X-CSRFToken": (document.querySelector(
                "input[name=csrfmiddlewaretoken]"
            )).value,
        },
    }).then(function (response) {
        if (response.status === 200) {
            // If message was deleted successfully, remove the div containing the message
            deletion_button.closest(".chat-message").remove();
        } else {
            // Throw error which will then be caught later
            throw new Error("Chat message could not be deleted: HTTP status " + response.status + " " + response.statusText);
        }
    }).catch(error => {
        console.log(error);
        if (error instanceof TypeError) {
            // Handle network error
            u('#chat-network-error').removeClass("hidden");
        } else {
            // Handle server error
            u('#chat-server-error').removeClass("hidden");
        }
    });
}
