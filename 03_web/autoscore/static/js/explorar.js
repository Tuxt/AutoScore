$('.run_score').click(function(){;
    var container = document.getElementById('embed-container');
    container.hidden = false;
    container.innerHTML = '';
    var embed = new Flat.Embed(container, {
        score: $(this).val(),
        embedParams: {
            appId: '5a1b1fbbcad0883e6b5ebc28',
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