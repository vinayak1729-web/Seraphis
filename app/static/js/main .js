$(document).ready(function () {
    $('#send_button').click(function () {
        var userInput = $('#user_input').val();
        if (userInput.trim()) {
            $('#chat-box').append('<div class="message user-message">' + userInput + '</div>');
            $('#user_input').val('');

            $.post('/chat', { user_input: userInput }, function (data) {
                $('#chat-box').append('<div class="message bot-message">' + data.response + '</div>');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            }).fail(function () {
                $('#chat-box').append('<div class="message bot-message">Sorry, an error occurred.</div>');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            });
        }
    });

    $('#user_input').keypress(function (e) {
        if (e.which == 13) {
            $('#send_button').click();
        }
    });
});