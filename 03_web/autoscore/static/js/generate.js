var nat_notes = [
    ['.note-re3', '=d'],
    ['.note-la2', '=A'],
    ['.note-si2', '=B'],
    ['.note-mi3', '=e'],
    ['.note-sol2', '=G'],
    ['.note-sol3', '=g'],
    ['.note-do3', '=c'],
    ['.note-la3', '=a'],
    ['.note-mi2', '=E'],
    ['.note-re2', '=D'],
    ['.note-fa3', '=f'],
    ['.note-si3', '=b'],
    ['.note-fa2', '=F'],
    ['.note-do2', '=C'],
    ['.note-si1', '=B,'],
    ['.note-la1', '=A,'],
    ['.note-do4', "=c'"],
    ['.note-sol1', '=G,'],
    ['.note-re4', "=d'"],
    ['.note-mi4', "=e'"]
    ];

var sharp_notes = [
    ['.note-fa3', '^f'],
    ['.note-do3', '^c'],
    ['.note-fa2', '^F'],
    ['.note-la2', '^A'],
    ['.note-sol3', '^g'],
    ['.note-sol2', '^G'],
    ['.note-re3', '^d'],
    ['.note-do2', '^C'],
    ['.note-la3', '^a'],
    ['.note-re2', '^D'],
    ['.note-do4', "^c'"],
    ['.note-la1', '^A,'],
    ['.note-sol1', '^G,']
    ];


$(document).ready(function(){

    textarea = $('#scoreNotes');

    for (let note in nat_notes) {
        $(nat_notes[note][0]).prop('disabled', false);
        
        $(nat_notes[note][0]).click(function(evt){
            mul = $('#duration').val();
            if (mul == "1") {
                mul = "";
            } else {
                mul += " ";
            }
            textarea.val(textarea.val() + nat_notes[note][1] + " " + mul);
        });
    }
});

// Prevent submit form when hit enter
$('#score-form').bind('keydown', function(e) {
    if (e.keyCode == 13) {
        e.preventDefault();
    }
});

$('#btn-sharp').click(function(){
    textarea = $('#scoreNotes');
    if ($(this).hasClass('active')) {
        $(this).removeClass('active').attr('aria-pressed',false);
        // Disable sharped notes
        for (let note in sharp_notes) {
            $(sharp_notes[note][0]).prop('disabled', true);
            $(sharp_notes[note][0]).unbind('click');
        }
        // Enable natural notes
        for (let note in nat_notes) {
            $(nat_notes[note][0]).prop('disabled', false);
            $(nat_notes[note][0]).click(function(){
                mul = $('#duration').val();
                if (mul == "1") {
                    mul = "";
                } else {
                    mul += " ";
                }
                textarea.val(textarea.val() + nat_notes[note][1]+" "+mul);
            });
        }
    } else {
        $(this).addClass('active').attr('aria-pressed',true);
        // Disable natural notes
        for (let note in nat_notes) {
            $(nat_notes[note][0]).prop('disabled', true);
            $(nat_notes[note][0]).unbind('click');
        }
        // Enable sharped notes
        for (let note in sharp_notes) {
            $(sharp_notes[note][0]).prop('disabled', false);
            $(sharp_notes[note][0]).click(function(){
                mul = $('#duration').val();
                if (mul == "1") {
                    mul = "";
                } else {
                    mul += " ";
                }
                textarea.val(textarea.val() + sharp_notes[note][1]+" "+mul);
            });
        }
    }
});

$('#btn-prob').click(function(){
    if ($(this).hasClass('active')) {
        $(this).removeClass('active').attr('aria-pressed', false);
    } else {
        $(this).addClass('active').attr('aria-pressed', true);
    }
});

$('#btn-erase').click(function(){
    textarea = $('#scoreNotes');
    data = textarea.val().split(" ");
    data.splice(-2,1);
    textarea.val(data.join(" "));
});

$('#btn-delete').click(function(){
    $('#scoreNotes').val("");
});


// Silence button
$('#btn-silence').click(function(){
    textarea = $('#scoreNotes');
    mul = $('#duration').val();
    if (mul == "1") {
        mul = "";
    } else {
        mul += " ";
    }
    textarea.val(textarea.val() + "z " + mul);
});

// Durations
removeIconDuration = function(index, className) {
    return (className.match(/(^|\s)icon-duration-\S+/g) || []).join(' ');
}
$('#select-duration-1').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-1');
    $('#duration').val("8");
});
$('#select-duration-2').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-2');
    $('#duration').val("6")
});
$('#select-duration-3').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-3');
    $('#duration').val("4")
});
$('#select-duration-4').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-4');
    $('#duration').val("3")
});
$('#select-duration-5').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-5');
    $('#duration').val("2")
});
$('#select-duration-6').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-6');
    $('#duration').val("3/2")
});
$('#select-duration-7').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-7');
    $('#duration').val("1")
});
$('#select-duration-8').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-8');
    $('#duration').val("/2")
});
$('#select-duration-9').click(function(){
    $('#duration-icon').removeClass(removeIconDuration);
    $('#duration-icon').addClass('icon-duration-9');
    $('#duration').val("/4")
});

// Triplet and quadruplet
$('#btn-triplet').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "(3 ");
});
$('#btn-quadruplet').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "(4 ");
});

// Tie
$('#btn-tie').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "- ");
});

// Roll
$('#btn-roll').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "~ ");
});

// Roll
$('#btn-fermata').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "H ");
});

// Trill
$('#btn-trill').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "T ");
});

// Chords
$('#btn-open-chord').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "[ ");
});

$('#btn-close-chord').click(function(){
    textarea = $('#scoreNotes');
    textarea.val(textarea.val() + "] ");
});


/* INSTRUMENTS */
/* Keyboards */
$('#select-instrument-piano').click(function(){
    $('#instrument').val("0").text("Piano");
    $('#program').val(0);
});

$('#select-instrument-organ').click(function(){
    $('#instrument').val("19").text("Organ");
    $('#program').val(19);
});

$('#select-instrument-celesta').click(function(){
    $('#instrument').val("8").text("Celesta");
    $('#program').val(8);
});

$('#select-instrument-harpsichord').click(function(){
    $('#instrument').val("6").text("Clavichord");
    $('#program').val(6);
});

/* Strings */
$('#select-instrument-violin').click(function(){
    $('#instrument').val("40").text("Violin");
    $('#program').val(40);
});

$('#select-instrument-viola').click(function(){
    $('#instrument').val("41").text("Viola");
    $('#program').val(41);
});

$('#select-instrument-ensemble').click(function(){
    $('#instrument').val("48").text("String ensemble");
    $('#program').val(48);
});

/* Woodwind */
$('#select-instrument-clarinet').click(function(){
    $('#instrument').val("71").text("Clarinet");
    $('#program').val(71);
});

$('#select-instrument-recorder').click(function(){
    $('#instrument').val("74").text("Recorder");
    $('#program').val(74);
});

/* Brass */
$('#select-instrument-brass-section').click(function(){
    $('#instrument').val("61").text("Brass section");
    $('#program').val(61);
});

$('#select-instrument-trumpet').click(function(){
    $('#instrument').val("56").text("Trumpet");
    $('#program').val(56);
});

/* Plucked strings */
$('#select-instrument-acoustic-guitar').click(function(){
    $('#instrument').val("25").text("Acoustic guitar");
    $('#program').val(25);
});

$('#select-instrument-classic-guitar').click(function(){
    $('#instrument').val("24").text("Classic guitar");
    $('#program').val(24);
});

$('#select-instrument-distortion-guitar').click(function(){
    $('#instrument').val("30").text("Distortion guitar");
    $('#program').val(30);
});

/* LOADING */
function openLoading() {
    $('#modalRun').modal('hide');
    document.getElementById('loading').style.display = "block";
}
