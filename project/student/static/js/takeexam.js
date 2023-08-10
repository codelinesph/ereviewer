/**
  JAVASCRIPT FOR TAKE EXAM DOCUMENT
  IMPORTANT: THE GOAL IS TO KEEP THIS THING READABLE!
  TRY TO USE AS MUCH NATIVE SCRIPT AS POSSIBLE TO KEEP IT'S LIFECYCLE LONGER
*/
$(function () {
  $('[data-toggle="popover"]').popover()
})

var questions = [];
var question_index = 0;
var view_mode = "list";
var exam_submitted = false;
var answered_all = false;
var overrides_incomplete=false;
var overall_points = 0;


/**
    DOM ELEMENTS
 */

// ALERT BOXES
// <editor-collapse>
    var alert_incomplete_exam = document.getElementById("exam-submit-incomplete");
    var alert_exam_submit_ok = document.getElementById("exam-submit-success");
    var alert_exam_submit_inf = document.getElementById("exam-submit-info");
    var alert_exam_tips = document.getElementById("exam-take-tips");

    // MAIN CONTAINERS
    var cont_reviewer = document.getElementById("questions-review-mode");
    var cont_reviewer_body = cont_reviewer.querySelectorAll(".c-body")[0];
    var cont_questionaire = document.getElementById("questions-holder");
    var cont_submit_progress = document.getElementById("cont-exam-submit-progressing");
    var cont_content_loading_progress = document.getElementById("content-load-progressing");

    // CONTROL BOXES
    var cont_ctr_footer = document.getElementById("footer-controls");
    var cont_ctr_point_nav = document.getElementById("point-controller-container");
    var cont_ctr_on_finish = document.getElementById("on-finish-toolbar");
    var cont_ctr_press_pagination = document.getElementById("press-view-navigator");
    var cont_ctr_view_options = document.getElementById("display-options");

    // INDIVIDUAL BUTTONS
    var btn_return_take = document.getElementById("return-to-take");
    var btn_submit_exam = document.getElementById("finalize-submit");
    var btn_return_home = document.getElementById("return-home");
    var btn_retake_exam = document.getElementById("retake-exam");

    // VIEW MODE BUTTONS
    var btn_viewm_list = cont_ctr_view_options.querySelectorAll('div')[0].querySelectorAll('div')[0].querySelectorAll('#set-list-view')[0];
    var btn_viewm_press = cont_ctr_view_options.querySelectorAll('div')[0].querySelectorAll('div')[0].querySelectorAll('#set-press-view')[0];
    var btn_viewm_grid = cont_ctr_view_options.querySelectorAll('div')[0].querySelectorAll('div')[0].querySelectorAll('#set-grid-view')[0];
// </editor-collapse>

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

function randomize_choices(questions){
    for(var i=0; i<questions.length;i++){
        questions[i].choices = shuffle(questions[i].choices);
    }
    return questions;
}
/**
  XMLHTTP OPERATION METHODS
 */
// gets all questionaires from api and stores into (var questions)
function get_questions(){
    url = location.protocol + '//' + location.host + location.pathname + '/getquestions';
    var xhttp; 
    if (window.XMLHttpRequest) {
        xhttp = new XMLHttpRequest();
    } else {
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    cont_content_loading_progress.classList.remove('d-none');
    cont_questionaire.classList.add('d-none');

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            questions = randomize_choices(JSON.parse(this.responseText));
            build_questions_dom_listview();

            cont_ctr_view_options.classList.remove("d-none");
            cont_ctr_footer.classList.remove("d-none");
            setFinishedToolbarsHidden(false);

            cont_content_loading_progress.classList.add('d-none');
            cont_questionaire.classList.remove('d-none');
        }
    };
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("Accept", "application/json");
    xhttp.send(); 
}

function returnToExam(){
    alert_incomplete_exam.classList.add('d-none');
    cont_reviewer.classList.add('d-none');
    cont_questionaire.classList.remove('d-none');
    btn_return_take.classList.add('d-none');
    cont_ctr_view_options.classList.remove('d-none');

    if(view_mode=='list'){

    }else if(view_mode=='press'){
        cont_ctr_press_pagination.classList.remove('d-none');
        cont_ctr_point_nav.classList.remove('d-none');
    }
    overrides_incomplete = false;
}

// submit exam method, contains ajax caller
function submitExam(){
    var cont = true;

    alert_exam_tips.classList.add('d-none');
    alert_incomplete_exam.classList.add('d-none');

    if(!answered_all && !overrides_incomplete){
        cont = false;

        alert_incomplete_exam.classList.remove('d-none');
        cont_reviewer.classList.remove('d-none');
        cont_questionaire.classList.add('d-none');
        btn_return_take.classList.remove('d-none');
        cont_ctr_press_pagination.classList.add('d-none');
        cont_ctr_point_nav.classList.add('d-none');
        cont_ctr_view_options.classList.add('d-none');

        overrides_incomplete = true;

        build_review_dom_table();
    }

    if(cont && confirm("Confirm Submission")){
        
        overrides_incomplete = false;
        var data = questions;
        data = JSON.stringify(data);

        btn_submit_exam.classList.add('d-none');
        btn_return_take.classList.add('d-none');
        cont_reviewer.classList.add('d-none');
        cont_ctr_footer.classList.add('d-none');

        cont_submit_progress.classList.remove('d-none');

        url = location.protocol + '//' + location.host + location.pathname + '/submitexam';
        var xhttp; 
        if (window.XMLHttpRequest) {
            xhttp = new XMLHttpRequest();
        } else {
            xhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                answers = JSON.parse(this.responseText);
                applyAnswers(answers);
                exam_submitted = true;
                setFinishedToolbarsHidden(true);

                cont_submit_progress.classList.add('d-none');

                btn_return_home.classList.remove('d-none');
                btn_retake_exam.classList.remove('d-none');

                alert_exam_submit_ok.classList.remove("d-none");
                alert_exam_submit_inf.classList.remove("d-none");

                cont_ctr_view_options.classList.remove('d-none');
                cont_ctr_footer.classList.remove('d-none');

                cont_questionaire.classList.remove('d-none');

                if(view_mode=='list'){

                }else if(view_mode=='press'){
                    cont_ctr_press_pagination.classList.remove('d-none');
                    cont_ctr_point_nav.classList.remove('d-none');
                }
            }
        };

        xhttp.open("POST", url, true);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.setRequestHeader("Accept", "application/json");
        xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhttp.send(data); 
    }
}
// method to read cookies from storage
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
  DOM RENDERER METHODS
 */
// Builds a card element for a question and its choices
function questionaire_card_render(e,i){
    card = document.createElement('div');
    card.className = "card rounded-0 mt-1 q-card-default shadow";
    card_body = document.createElement('div');
    card_body.className = "card-body p-0";
    card_body.innerHTML =
        '<div class="p-3">'+
        '<strong>Question#'+(parseInt(i)+1)+': </strong><br>'+
        e.question+
        '</div>'+
        '<small class="ml-3">Choices <strong>(Choose '+(e.expected_answers)+')</strong>:</small>';
    answers_ul = document.createElement('ul');
    answers_ul.className = "list-group list-group-flush";

    if(e.choices){
        for(ci=0;ci<e.choices.length;ci++){
            ce = e.choices[ci];

            choice = document.createElement('a');
            choice.className = "list-group-item text-dark q-card-choice";

            if(ce.my_answer) {
                choice.classList.add("bdr-selected");
            }
            
            choice.href = "javascript:void(0)";
            choice.setAttribute("data-ci",ci);
            choice.setAttribute("data-cq",i);
            choice.addEventListener("click", set_answer);
            choice.innerHTML = ce.answer;
            ce.elm = choice;
            answers_ul.appendChild(ce.elm);
        }
    }
    card_body.appendChild(answers_ul);
    card.appendChild(card_body);

    return card;
}
// Builds a list of questionaires for list-view-mode
function build_questions_dom_listview(){
    view_mode = "list";

    cont_ctr_press_pagination.classList.add("d-none");
    cont_questionaire.classList.remove("card-columns");
    cont_ctr_point_nav.classList.add("d-none");
    alert_exam_tips.classList.remove("d-none");

    questions_container = document.getElementsByClassName('questionaires')[0];
    questions_container.innerHTML = "";
    
    if(questions && questions.length>0){
        for(i=0;i<questions.length;i++){
            e=questions[i]
            var card = questionaire_card_render(e,i);
            e.elm = card;
            questions_container.appendChild(e.elm);
        }
    }
    if(exam_submitted){
        renderFinalized();
    }
}
// Builds a question card based on (var question_index) index specific
function build_questions_dom_pressview(init_controller = true){

    if(init_controller){
        view_mode = "press";
        cont_ctr_press_pagination.classList.remove("d-none");
        cont_questionaire.classList.remove("card-columns");
        cont_ctr_point_nav.classList.remove("d-none");
        alert_exam_tips.classList.remove("d-none");
    }

    questions_container = document.getElementsByClassName('questionaires')[0];
    questions_container.innerHTML = "";
    disablePointControllers();
    if(question_index>=0 && question_index<questions.length-1){
        enablePointController(document.getElementById("press-view-next"));
    }
    if(question_index>0 && question_index<=questions.length-1){
        enablePointController(document.getElementById("press-view-prev"));
    }
    if(questions[question_index]){
        e = questions[question_index];
        var card = questionaire_card_render(e,question_index);
        questions[question_index].elm = card;

        questions_container.appendChild(card);

        renderPressViewNavigator();
        evaluateAnswers();
    }
    if(exam_submitted){
        renderFinalized();
    }
}

// Builds review mode table
function build_review_dom_table(){
    // lets initialize the table element first
    var table = document.createElement("table");
    // then set basic classes
    table.className = "table table-hover table-bordered p-0 m-0 bg-white";

    // now we will render the table header
    table_header = document.createElement("tr");
    table_header.innerHTML = "<th>-</th><th>Question</th><th>My Answer/s</th>";

    // then render header into main table
    table.append(table_header);

    // now we will render the questionaires
    if(questions && questions.length>0){
        for(i=0;i<questions.length;i++){

            var question = questions[i];
            var row = document.createElement("tr");
            var answer_count = 0;
            var has_answer = false;

            for(ci=0;ci<question.choices.length;ci++){
                var choice = question.choices[ci];
                if(choice.my_answer){
                    answer_count++;
                    has_answer = true;
                }
            }

            if(answer_count==0){
                answer_count = 1;
            }

            var col_question = document.createElement("td");
            var col_numbering = document.createElement("td");
            col_question.setAttribute('rowspan',answer_count);
            col_numbering.setAttribute('rowspan',answer_count);

            col_question.innerHTML = question.question;
            col_numbering.innerHTML = i+1;
            row.prepend(col_question);
            row.prepend(col_numbering);
            
            if(has_answer){
                var asc = 0;
                for(ci=0;ci<question.choices.length;ci++){
                    var choice = question.choices[ci];
                    if(choice.my_answer){
                        if(asc==0){
                            var col_choice = document.createElement("td");
                            col_choice.innerHTML = choice.answer;
                            row.append(col_choice);
                            table.append(row);
                        }else{
                            var col_choice_row = document.createElement("tr");
                            var col_choice = document.createElement("td");
                            col_choice.innerHTML = choice.answer;
                            col_choice_row.append(col_choice);
                            table.append(col_choice_row);
                        }
                        asc++;
                    }
                } 
            }else{
                var col_unanswered = document.createElement("td");
                col_unanswered.innerHTML = "<strong>(No Answer)</strong>";
                row.append(col_unanswered);
                table.append(row);
            }
        }
    }


    // lastly, clear and render the entire section into the dom
    cont_reviewer_body.innerHTML = "";
    cont_reviewer_body.append(table);
}


/**
  EVENT CALLBACK METHODS FOR DYNAMIC DOM ELEMENTS
 */
// function called when a choice is selected by the user
function set_answer(evt){
    var ci = evt.target.getAttribute("data-ci");
    var cq = evt.target.getAttribute("data-cq");
    if(questions[cq]){
        var question = questions[cq];
        if(question.choices[ci]){
            var choice = question.choices[ci];
            if(choice.my_answer){
                choice.my_answer = false;
                evt.target.classList.remove("bdr-selected");
            }else{
                var current_answers = 0;
                for(i=0;i<question.choices.length;i++){
                    if(question.choices[i].my_answer){
                        current_answers++;
                    }
                }
                if(current_answers<question.expected_answers){
                    choice.my_answer = true;
                    evt.target.classList.add("bdr-selected");
                }
            }
        }
    }
    evaluateAnswers();
}


/**
  VIEW TYPE ACTION METHODS
  @recommendation : merge into one function
 */
//sets all view controller buttons to enabled state
function enableControllers(){
    var viewcontrollers = document.getElementsByClassName("view-controller");
    for(i=0;i<viewcontrollers.length;i++){
        viewcontrollers[i].classList.remove("btn-dark");
        viewcontrollers[i].classList.add("btn-outline-dark");
        viewcontrollers[i].disabled = false;
    }
}
//sets a specific view controller button to disabled state
function disableController(e){
    e.classList.remove("btn-outline-dark");
    e.classList.add("btn-dark");
    e.disabled = true;
}


/**
  PRESS VIEW MODE CONTROLLER METHODS
 */
// sets all controller elements state to disabled
// @param disable?(true/false)
// @recommendation : merge with enablePointController()
function disablePointControllers(e=false){
    if(e){
        e.disabled = true;
    }else{
        var pointer = document.getElementsByClassName("point-controller");
        for(i=0;i<pointer.length;i++){
            pointer[i].disabled = true;
        }
    }
}
// sets a specific controller element state to enabled
// @param : the element to disable
function enablePointController(e){
    e.disabled = false;
}
// renders pagination for press view
function renderPressViewNavigator(){
  var nav_containment = cont_ctr_press_pagination.querySelectorAll(".pagination")[0];
  nav_containment.innerHTML = null;
  for(i=0;i<questions.length;i++){
        var question = questions[i];
        var answered = 0;
        for(ci=0;ci<question.choices.length;ci++){
            if(question.choices[ci].my_answer){
                answered++;
            }
        }

        navigator_wrapper = document.createElement("li");
        navigator_anchor = document.createElement("a");

        navigator_wrapper.className = "page-item";
        navigator_anchor.className = "page-link rounded-0";

        if(i==question_index){
            navigator_wrapper.classList.add("active");
        }
        if(answered==question.expected_answers){
            navigator_anchor.classList.add("border-success");
            navigator_anchor.classList.add("text-success");
        }

        navigator_anchor.href = "javascript:void(0)";
        navigator_anchor.innerHTML = (i+1);
        navigator_anchor.setAttribute("data-id",i);

        navigator_anchor.addEventListener("click",function(evt){
            question_index = evt.target.getAttribute("data-id");
            build_questions_dom_pressview(false);
        });
        
        navigator_wrapper.appendChild(navigator_anchor);
        nav_containment.appendChild(navigator_wrapper);
    }
}


// "finished" exam toolbar methods
function setFinishedToolbarsHidden(st=false){
    var toolbar = cont_ctr_on_finish;
    if(st){
        toolbar.classList.add("d-none");
    }else{
        toolbar.classList.remove("d-none");
    }
}


/**
  ANSWER EVALUATION METHODS
 */

// evaluates all question if it is answered and marks the cards according to its status
// also contains the triggers for "finished button"
function evaluateAnswers(){
    var completed = 0;
    for(i=0;i<questions.length;i++){
        var question = questions[i];
        answers = 0;
        for(ci=0;ci<question.choices.length;ci++){
            choice = question.choices[ci];
            if(choice.my_answer){
                answers++;
            }
        }
        if(answers>=question.expected_answers){
            completed++;
            question.elm.classList.remove("q-card-default");
            question.elm.classList.add("q-card-completed");
        }else{
            completed--;
            question.elm.classList.remove("q-card-completed");
            question.elm.classList.add("q-card-default");
        }
    }
    answered_all = (completed>=questions.length);

    if(exam_submitted){
        setFinishedToolbarsHidden(true);
    }
    if(view_mode=="press"){
        renderPressViewNavigator();
    }else if(view_mode=="list"){

    }
}
// event callback when an answer button is selected/clicked
function applyAnswers(answers){
    for(ia=0;ia<answers.length;ia++){
        var answer = answers[ia];
        for(iq=0;iq<questions.length;iq++){
            var question = questions[iq];
            if(question.id==answer.id){
                var points = 0;
                var correct_answers = 0;

                for(iac=0;iac<answer.choices.length;iac++){
                    var corrected_choice = answer.choices[iac];
                    for(iqc=0;iqc<question.choices.length;iqc++){
                        answered_choice = question.choices[iqc];
                        if(answered_choice.id==corrected_choice.id){
                            if(corrected_choice.is_correct_answer){
                                if(answered_choice.my_answer){
                                    correct_answers++;
                                    points++;
                                }

                                if(corrected_choice.reasons) answered_choice.reasons = corrected_choice.reasons;
                                else answered_choice.reasons = "N/A";
                                if(corrected_choice.links) answered_choice.links = corrected_choice.links;
                                else answered_choice.links = "N/A";

                                answered_choice.is_correct_answer = corrected_choice.is_correct_answer
                                
                            }
                        }
                    }
                }
                question.points = points/answer.expected_answers;
                overall_points += question.points;
                if(parseInt(correct_answers) == parseInt(answer.expected_answers)){
                    question.im_correct = true;
                }else{
                    question.im_correct = false;
                }
            }
        }
    }
    renderFinalized();
}
// renders the finalized answers with the response from server through ajax
function renderFinalized(){
    alert_exam_tips.classList.add("d-none");
    // gets all q-card choice buttons
    var choice_elements = document.getElementsByClassName("q-card-choice");
    // removes all event listener to render the buttons unusable
    for(i=0;i<choice_elements.length;i++){
        choice_elements[i].removeEventListener("click",set_answer);
    }
    // now we will loop though all the questions
    for(i=0;i<questions.length;i++){
        var question = questions[i];
        // removes default classname of binded q-card
        question.elm.classList.remove("q-card-default");
        // adds classname depending on the state of correctness
        if(question.im_correct){
            question.elm.classList.add("q-card-correct");
        }else{
            question.elm.classList.add("q-card-incorrect");
        }
        // now lets loop trough choices
        for(ci=0;ci<question.choices.length;ci++){
            var choice = question.choices[ci];
            var content = choice.elm.innerHTML;

            // resets styling and content and flexes
            choice.elm.innerHTML = "";
            choice.elm.classList.remove('bdr-selected');
            choice.elm.classList.add('d-flex');
            choice.elm.classList.add('justify-content-between');

            // generates new elements that will contain pharagraph and icon
            var phar = document.createElement("span");
            var icon = document.createElement("span");
            // keep the icon on the right side
            icon.className = "text-right";
            phar.innerHTML = content;

            /* 
                if the choice is the correct answer but its not my answer
                add the popover and all the stylings
            */
            if(choice.is_correct_answer && !choice.my_answer){
                choice.elm.classList.add('bdr-correct_answer');

                choice.elm.setAttribute('data-toggle','popover');
                choice.elm.setAttribute('data-trigger','focus');
                choice.elm.setAttribute('data-placement','top');
                choice.elm.setAttribute('data-content',choice.reasons);
                choice.elm.setAttribute('title','Correct Answer Explanation');

                $(choice.elm).popover();
                
                icon.innerHTML = '<i class="far fa-hand-point-left"></i><small>&nbsp;&nbsp;Correct Answer</small>';
            }
            /* 
                if the choice is the correct answer and its my answer
                add the stylings for correct
            */
            else if(choice.is_correct_answer && choice.my_answer){
                choice.elm.classList.add('bdr-im_correct');
                icon.innerHTML = '<i class="fas fa-check"></i>';
            }
            /* 
                if the choice is not the correct answer and its my answer
                add the stylings for incorrect
            */
            else if(!choice.is_correct_answer && choice.my_answer){
                choice.elm.classList.add('bdr-im_wrong');
                icon.innerHTML = '<i class="fas fa-times"></i>';
            }
            // then append it to the list item
            choice.elm.appendChild(phar);
            choice.elm.appendChild(icon);
        }

        // lets now generate card header containing my points
        var card_header = document.createElement("div");
        card_header.className = "card-header text-right rounded-0 p-1";
        card_header.innerHTML = question.points.toFixed(2)+" pt/s.";
        // then append it to the card
        question.elm.prepend(card_header);

    }
    // now we will show and hide all the necessary dom elements
    document.getElementById("exam-summary-score").innerHTML = overall_points + "/" + questions.length;
    document.getElementById("exam-summary-percentage").innerHTML = ((overall_points/questions.length)*100)+"%";
    document.getElementById("exam-summary-container").classList.remove("d-none");
    document.getElementsByTagName("html").scrollTop = 0;
}


/**
  EVENT LISTENERS
 */
btn_viewm_list.addEventListener("click", function(e){
    build_questions_dom_listview();
    enableControllers();
    evaluateAnswers();
    disableController(this);
});
document.getElementById("set-grid-view").addEventListener("click", function(e){
    build_questions_dom_listview();
    cont_ctr_press_pagination.classList.add("d-none");
    cont_questionaire.classList.add("card-columns");
    view_mode = "list";

    enableControllers();
    evaluateAnswers();
    disableController(this);
});
document.getElementById("set-press-view").addEventListener("click", function(e){
    question_index = 0;
    build_questions_dom_pressview();
    enableControllers();
    disableController(this);
});


document.getElementById("press-view-prev").addEventListener("click", function(e){
    question_index--;
    build_questions_dom_pressview(false);
});
document.getElementById("press-view-next").addEventListener("click", function(e){
    question_index++;
    build_questions_dom_pressview(false);
});
document.getElementById("start-exam").addEventListener("click", function(e){
    get_questions();
    this.classList.add("d-none"); 
});


window.onbeforeunload = function(){
    if(!exam_submitted){
        return 'Are you sure you want to leave?';
    }
};