/**
 * Created by sponugot on 3/14/16.
 */
$(document).ready(function () {
    toggleFields();
    $("#id_greeting_type").change(function () {
        toggleFields();
    });

});
//To change the customization form based on greeting_type change
function toggleFields() {
    if ($("#id_greeting_type").val() == 'e') {
        $("#email").show();
        $("#sms").hide();
    }
    else {
        $("#email").hide();
        $("#sms").show();
    }
}


