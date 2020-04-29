$(function() {
    $('#donate-model').on("show.bs.modal", function (e) {
        // $('.modal-backdrop').remove()
        console.log("UUUUUU1")
        $("#donateModalLabel").html("Donation Confirmation");
        $("#project-title").html($(e.relatedTarget).data('title'));
        $("#project_id").val($(e.relatedTarget).data('project_id'))
        $("#donation-val").attr({
            max:$(e.relatedTarget).data('target-donation')-$(e.relatedTarget).data('current-donation'),
            min:1
        })

        setTimeout(()=>{
            $('.modal-backdrop').remove()
        },200)
        // $("body").remove()
    });
});
