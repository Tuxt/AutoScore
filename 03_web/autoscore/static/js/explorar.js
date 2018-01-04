$('.run_score').click(function(){;
    var container = document.getElementById('embed-container');
    container.hidden = false;
    container.innerHTML = '';
    var embed = new Flat.Embed(container, {
        score: $(this).val(),
        embedParams: {
            appId: '<<app_id>>',
            controlsFloating: false
        }
    });
    embed.ready().then(closeLoading());
});

function openLoading() {
    document.getElementById('loading').style.display = "block";
}
function closeLoading() {
    setTimeout(function(){
        document.getElementById('loading').style.display = "none";
    },3000);
}