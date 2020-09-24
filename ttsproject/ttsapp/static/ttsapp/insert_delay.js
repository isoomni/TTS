function getInputSelection(el) {
    var start = 0, end = 0, normalizedValue, range,
        textInputRange, len, endRange;

    if (typeof el.selectionStart == "number" && typeof el.selectionEnd == "number") {
        start = el.selectionStart;
        end = el.selectionEnd;
    } else {
        range = document.selection.createRange();

        if (range && range.parentElement() == el) {
            len = el.value.length;
            normalizedValue = el.value.replace(/\r\n/g, "\n");

            // Create a working TextRange that lives only in the input
            textInputRange = el.createTextRange();
            textInputRange.moveToBookmark(range.getBookmark());

            // Check if the start and end of the selection are at the very end
            // of the input, since moveStart/moveEnd doesn't return what we want
            // in those cases
            endRange = el.createTextRange();
            endRange.collapse(false);

            if (textInputRange.compareEndPoints("StartToEnd", endRange) > -1) {
                start = end = len;
            } else {
                start = -textInputRange.moveStart("character", -len);
                start += normalizedValue.slice(0, start).split("\n").length - 1;

                if (textInputRange.compareEndPoints("EndToEnd", endRange) > -1) {
                    end = len;
                } else {
                    end = -textInputRange.moveEnd("character", -len);
                    end += normalizedValue.slice(0, end).split("\n").length - 1;
                }
            }
        }
    }

        return {
            start: start,
            end: end
        };
    }



function make_btn_events(first_tag, second_tag=null) {
    var input = document.getElementById("body");
    var input_text = input.value;
    // var input_length = input_text.length;

    input.focus();
    var result = getInputSelection(input);
    // var resultSpan = document.getElementById("result");

    if (second_tag == null) {
        var output = [input_text.slice(0, result.start), first_tag, input_text.slice(result.start)].join('');
    } else {
        var output = [input_text.slice(0, result.start), first_tag, input_text.slice(result.start, result.end), second_tag, input_text.slice(result.end)].join('');
    }
     
    // textarea에 delay 삽입
    input.value = output;
    
    // 현재 cursor 위치 = result.start
    // 드래그 했을 때 cursor의 마지막 위치 = result.end

    // if (result.start == result.end){
    //     resultSpan.innerHTML = "No text selected. Position of cursor is " + result.start +" of " + input_length;
    // }else{
    //     resultSpan.innerHTML = "You've selected text ("+result.start+" to "+ result.end +") from a total length of " + input_length;
    // }
}

document.getElementById("btn_delay").addEventListener("click", function() {make_btn_events("<break time=\"1s\"/>")}, false);
document.getElementById("btn_strong").addEventListener("click", function() {make_btn_events("<emphasis level=\"strong\">", "</emphasis>")}, false);
document.getElementById("btn_slow").addEventListener("click", function() {make_btn_events("<prosody rate=\"slow\">", "</prosody>")}, false);
document.getElementById("btn_cardinal").addEventListener("click", function() {make_btn_events("<say-as interpret-as=\"cardinal\">", "</say-as>")}, false);
document.getElementById("btn_ordinal").addEventListener("click", function() {make_btn_events("<say-as interpret-as=\"ordinal\">", "</say-as>")}, false);