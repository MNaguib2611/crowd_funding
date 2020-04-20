console.log();

$("#cat_selector").change(function (e) {
    console.log(e.currentTarget.value)
    window.location.href = `home?cat_id=${e.currentTarget.value}`
})