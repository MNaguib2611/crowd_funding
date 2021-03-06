$('#project_search').on('input', function (e) {
    if ($(this).val().trim().length === 0) {
        $("#projects_list").empty()
        return
    }
    $.ajax({
        url: 'search',
        data: {
            searchValue: $(this).val()
        },
        success: function (res) {
            $("#projects_list").empty()
            res.forEach((project) => {
                $("#projects_list").append(`<div class="pl-2"><h4 id="${project.id}" ><a href="/projects/${project.id}">${project.title}</a></h4> 
                        <h6 class="card-subtitle mb-1">Total Target: ${project.target}$</h6>
                            <h6 class="card-subtitle ">Current Target: ${project.current}$</h6></div><hr class="dashed">`)
            })
        }
    })
})
