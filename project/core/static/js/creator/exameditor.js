
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
let token = getCookie('csrftoken');
axios.defaults.headers.common['Accept'] = "application/json";

if (token) {
    axios.defaults.headers.common['X-CSRFToken'] = token;
} else {
    console.warn('CSRF token not found');
} 

$(document).ready(function(){
    let cont_questions = $("#questions-creator-container");
    let cont_add_questions = $("#add-question-container");

    let form_save_new_question = $("#new-question-main-formset");
    let form_exam_details = $("#exam-details-formset");

    let btn_new_question_add_answer = $("#new-question-add-answer");
    let btn_discard_changes = $("#edit-question-discard");
    let btn_backtop = $("#backtop");

    let ul_new_question_answers = $("#new-question-answers-ul");

    let modal_correct_answer_reason = $("#correct-answer-reason");

    let content_edit_mode = {
        onedit: false,
        data:{}
    };

    let data = [];

    let new_question_answers = [];

    function getExamData(){
        axios.get(studio_api+'examdata/'+exam_id)
        .then(function (response) {
            data = response.data.questions;
            render_questionaire();
        })
        .catch(function (error) {
            
        })
    }

    function scrollToAnchor(id){
        let elem = $("#"+id);
        if(elem.offset()){
            $('html, body').animate({
                scrollTop: elem.offset().top
            }, 500);
        }
    }
    function scrollToElem(elem){
        if(elem.offset()){
            $('html, body').animate({
                scrollTop: elem.offset().top
            }, 500);
        }
    }

    function render_answers_ul(answers){
        let ul = $(document.createElement("ul")).addClass("list-group list-group-flush mt-3");
        $.each(answers,function(i,v){
            let li = $(document.createElement("li")).addClass("list-group-item");
            li.html(v.answer);
            
            if(v.is_correct_answer){
                li.addClass("bg-success text-light");
                let info_btn = $(document.createElement("button"));
                info_btn.addClass("btn btn-light rounded-0");
                info_btn.attr({
                    "type":"button",
                    "data-toggle":"popover",
                    "data-trigger":"focus",
                    "title":"Correct Answer Explanation",
                    "data-content":v.reasons,
                });
                info_btn.html('<i class="fas fa-info"></i>');
                info_btn.popover();
                li.prepend("&nbsp;&nbsp;");
                li.prepend(info_btn);
            }

            ul.append(li);
        });
        return ul;
    }
    function render_question_card(question,reference,idx){
        let answers = question.answers;
        let card = $(document.createElement("div")).addClass("card rounded-0 mt-3 border-dark shadow");
        let card_body = $(document.createElement("div")).addClass("card-body");
        let card_footer = $(document.createElement("div")).addClass("card-footer");
        let btn_container = $(document.createElement("div")).addClass("btn-group");
        let ref_data = reference;
        card.attr({
            'id':"question-card-"+idx
        });
        btn_container.append(
            $(document.createElement("button"))
            .addClass("btn rounded-0 btn-outline-danger")
            .html("Delete").on("click",function(e){
                delete_question(e,ref_data);
            })
        );
        btn_container.append(
            $(document.createElement("button"))
            .addClass("btn rounded-0 btn-outline-primary")
            .html("Edit").on("click",function(e){
                edit_question(e,ref_data)
            })
        );

        card_body.append(question.question);
        card_body.append(render_answers_ul(question.answers));
        card_footer.append(btn_container);

        card.append(card_body);
        card.append(card_footer);

        question.element = card;

        return card;
    }
    function render_questionaire(){
        cont_questions.html("");
        $.each(data,function(i,v){
            let card = render_question_card(v,this,i);
            cont_questions.prepend(card);
        });
    }


    function edit_question(e,q,i){
        content_edit_mode.onedit = true;
        content_edit_mode.data = q;
        content_edit_mode.index = i;
        form_save_new_question.find("[name='question']").val(q.question);
        new_question_answers = q.answers;
        render_new_q_answers_ul();
        scrollToAnchor("top-anchor");
        btn_discard_changes.removeClass("d-none");
    }
    function delete_question(e,q){
        if(confirm("are you sure you want to delete this question?")){
            axios.delete(studio_api+'question/'+q.id+'/')
            .then(function (response) {
                data.splice(q,1);
                q.element.remove();
                toastr.success('Successfully Deleted!');
            })
            .catch(function (error) {
                toastr.error(error);
            })
        }
    }
    function delete_answer(e,ref_data,li){
        if(
            confirm("are you sure you want to delete this answer?")
        ){
            if(ref_data.id){
                axios.delete(studio_api+'answer/'+ref_data.id+'/')
                .then(function (response) {
                    new_question_answers.splice(ref_data,1);
                    li.remove();
                    toastr.success('Successfully Deleted!');
                })
                .catch(function (error) {
                    toastr.error(error);
                })
            }else{
                new_question_answers.splice(ref_data,1);
                li.remove();
                toastr.success('Successfully Deleted!');
            }
        }
    }


    function new_question_answer_onchange(e,r){
        r.answer = $(e).val();
    }
    function new_question_reason_onsubmit(e,r){
        let formdata_unindexed = $(e).serializeArray();
        let formdata = {};
        $.map(formdata_unindexed, function(n, i){
            formdata[n['name']] = n['value'];
        });
        r.reasons = formdata.reasons;
        r.links = formdata.links;
        modal_correct_answer_reason.modal('hide');
    }

    function render_new_q_answers_ul(){
        ul_new_question_answers.html("");
        $.each(new_question_answers, function(i,v){
            let ref_data = v;
            let li = $(document.createElement("li"))
            .addClass("list-group-item p-1")
            .append(
                $(document.createElement("div")).addClass("input-group")
                .append(
                    $(document.createElement("div"))
                    .addClass("input-group-prepend")
                    .append(
                        $(document.createElement("button"))
                        .addClass("btn rounded-0 "+((ref_data.is_correct_answer) ? "btn-primary" : "btn-outline-primary"))
                        .attr({
                            "type":"button",
                        })
                        .html('<i class="fas fa-arrow-right"></i>')
                        .on("click",function(e){
                            ref_data.is_correct_answer = !ref_data.is_correct_answer;
                            $(this)
                            .removeClass(["btn-primary","btn-outline-primary"])
                            .addClass(((ref_data.is_correct_answer) ? "btn-primary" : "btn-outline-primary"))
                        })
                    )
                    .append(
                        $(document.createElement("button"))
                        .addClass("btn rounded-0 btn-outline-info")
                        .attr({
                            "type":"button",
                            "title":"Reasons why this is the correct answer"
                        })
                        .html('<i class="fas fa-info"></i>')
                        .on("click",function(e){
                            modal_correct_answer_reason.modal('show');
                            let form = modal_correct_answer_reason.children('form');
                            form.find("[name='reasons']").val(ref_data.reasons);
                            form.find("[name='links']").val(ref_data.links);
                            form.off("submit")
                            .on("submit",function(e){
                                e.preventDefault();
                                new_question_reason_onsubmit(this,ref_data);
                            });
                        })
                    )
                )
                .append(
                    $(document.createElement("input"))
                    .addClass("rounded-0 form-control")
                    .attr({
                        "required":true,
                        "type":"text",
                    })
                    .val(v.answer)
                    .on("change",function(e){
                        new_question_answer_onchange(this,ref_data);
                    })
                )
                .append(
                    $(document.createElement("div"))
                    .addClass("input-group-append")
                    .append(
                        $(document.createElement("button"))
                        .addClass("btn rounded-0 btn-outline-danger")
                        .attr({
                            "type":"button",
                        })
                        .html('<i class="fas fa-times"></i>')
                        .on("click",function(e){delete_answer(this,ref_data,li);})
                    )
                )
            );
            ul_new_question_answers.append(li);
        });
    }

    function after_question_data_save(frm){
        $(frm).trigger("reset");
        new_question_answers = [];
        render_new_q_answers_ul();
        render_questionaire();

        if(content_edit_mode.onedit){
            scrollToAnchor("question-card-"+content_edit_mode.index);
            content_edit_mode = {
                onedit: false,
                data:{}
            };
        }

        btn_discard_changes.addClass("d-none");
    }

    form_save_new_question.submit(function(e){
        e.preventDefault();
        let form = this;
        let formdata_unindexed = $(this).serializeArray();
        let formdata = {};
        $.map(formdata_unindexed, function(n, i){
            formdata[n['name']] = n['value'];
        });
        formdata.exam = exam_id;
        if(content_edit_mode.onedit){
            content_edit_mode.data.answers = new_question_answers;
            content_edit_mode.data.question = formdata.question;
            axios.put(studio_api+'question/'+content_edit_mode.data.id+'/',content_edit_mode.data)
            .then(function (response) {
                toastr.success('Successfully Saved Edit!');
                scrollToElem(content_edit_mode.data.element);
                after_question_data_save(form);
            })
            .catch(function (error) {
                toastr.error(error);
            })
        }else{
            formdata.answers = new_question_answers;
            axios.post(studio_api+'question/',formdata)
            .then(function (response) {
                data.push(response.data);
                toastr.success('Successfully Saved New Data!');
                after_question_data_save(form);
            })
            .catch(function (error) {
                toastr.error(error);
            })
        }
    });
    form_exam_details.submit(function(e){
        e.preventDefault();
        if(confirm("are you sure you want to save this changes?")){
            let form = $(this)
            let formdata_unindexed = form.serializeArray();
            let formdata = {};

            $.map(formdata_unindexed, function(n, i){
                formdata[n['name']] = n['value'];
            });

            axios.put(studio_api+'exam/'+exam_id+'/',formdata)
            .then(function (response) {
                toastr.success('Successfully Saved Edit!');
            })
            .catch(function (error) {
                toastr.error(error);
            })
        }
    });

    btn_new_question_add_answer.on("click",function(){
        new_question_answers.push({
            answer:"",
            is_correct_answer:false,
            reasons:"",
        });
        render_new_q_answers_ul();
    });
    btn_discard_changes.on("click",function(){
        if(confirm("Are you sure you want to discard these changes?")){
            $(this).addClass("d-none");
            content_edit_mode = {
                onedit: false,
                data:{}
            };
            form_save_new_question.trigger("reset");
            new_question_answers = [];
            render_new_q_answers_ul();
        }
    })
    btn_backtop.on("click", function(){
        scrollToAnchor("top-anchor");
    });

    getExamData();
});