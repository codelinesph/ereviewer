$(document).ready(function(){
    let buttons = {
        individual:{
            return_take : $("#return-to-take"),
            submit_exam : $("#finalize-submit"),
            return_home : $("#return-home"),
            retake_exam : $("#retake-exam"),
            start_exam : $("#start-exam"),
            backtop: $("#backtop")
        },
        viewboxes:{
            btn_viewm_list : $('#set-list-view'),
            btn_viewm_press : $('#set-press-view'),
            btn_viewm_grid : $('#set-grid-view'),
        },
        groups:{
            btns_viewm : $(".view-controller"),
            btns_point_ctrl: $(".point-controller")
        }
    }
    let containers = {
        root: $("#root"),
        main:{
            reviewer : $("#questions-review-mode"),
            reviewer_body : $("#questions-review-mode").find(".card-body"),
            questionaire : $("#questions-holder"),
            submit_progress : $("#cont-exam-submit-progressing"),
            content_loading_progress : $("#content-load-progressing"),
        },
        controls:{
            footer : $("#footer-controls"),
            point_nav : $("#point-controller-container"),
            on_finish : $("#on-finish-toolbar"),
            press_pagination : $("#press-view-navigator"),
            view_options : $("#display-options"),
        },
        summary:{
            exam_summary:$('#exam-summary-container'),
            exam_score:$('#exam-summary-score'),
            exam_percentage:$('#exam-summary-percentage'),
        }
    }
    let alerts = {
        alert_incomplete_exam : $("#exam-submit-incomplete"),
        alert_exam_submit_ok : $("#exam-submit-success"),
        alert_exam_submit_inf : $("#exam-submit-info"),
        alert_exam_tips : $("#exam-take-tips"),
    }
    let tools = {
        shuffle:function(array){
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
        },
        randomize_choices:function(questions){
            for(var i=0; i<questions.length;i++){
                questions[i].choices = tools.shuffle(questions[i].choices);
            }
            return questions;
        },
        getCookie:function(name) {
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
    }
    var questions = [];

    let submitted = false;
    let default_view = 'press';

    //initial setup for axios
    axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    let token = tools.getCookie('csrftoken');
    axios.defaults.headers.common['Accept'] = "application/json";
    if (token) axios.defaults.headers.common['X-CSRFToken'] = token;
    else console.warn('CSRF token not found');

    // $('#global-request-loader-modal').modal({
    //     keyboard: false,
    //     backdrop: 'static',
    // });
    // Add a request interceptor
    axios.interceptors.request.use(function (config) {
        // $('#global-request-loader-modal').modal('show');
        return config;
    }, function (error) {
        // $('#global-request-loader-modal').modal('hide');
        toastr.error(error);
        return Promise.reject(error);
    });
    
    // Add a response interceptor
    axios.interceptors.response.use(function (response) {
        // $('#global-request-loader-modal').modal('hide');
        return response;
    }, function (error) {
        // $('#global-request-loader-modal').modal('hide');
        toastr.error(error);
        return Promise.reject(error);
    });

    let xhttp = {
        get_questions:function(){
            axios.get(location.pathname+'/getquestions')
            .then(function (response) {
                questions = tools.randomize_choices(response.data);
                // render_exam_listview();
                switch_to_default_view();
            })
        },
        submit_exam:function(callback = function(){return false;}){
            axios.post(location.pathname+'/submitexam',questions)
            .then(callback)
        }
    }

    // DOM ACTIONS
    function set_answer(t,e,choice,question){
        let ans = 0;
        $.each(question.choices,function(i,v){if(v.my_answer) ans++});

        if(choice.my_answer){
            choice.my_answer = false;
            $(t).removeClass('bdr-selected');
            ans--;
        }else{
            if(ans<question.expected_answers){
                choice.my_answer = true;
                $(t).addClass('bdr-selected');
                ans++;
            }
        }
        if(ans<question.expected_answers){
            question.__card.removeClass('q-card-completed');
            question.__card.addClass('q-card-default');
            question.__completed = false;
        }else{
            question.__card.addClass('q-card-completed');
            question.__card.removeClass('q-card-default');
            question.__completed = true;
        }
    }
    function scrollToTarget(target){
        if(target.offset()){
            $('html, body').animate({
                scrollTop: target.offset().top - 200
            }, 500);
        }
    }

    // DOM RENDERERS
    function render_exam_card(question){
        if(!submitted){
            question.__card = $(document.createElement('div'))

            .addClass('card rounded-0 mt-1 q-card-default shadow')
            .append(
                $(document.createElement('div'))
                .addClass('card-body p-0')
                .html(
                    '<div class="p-3">'+
                    '<strong>Question#'+(parseInt(questions.indexOf(question))+1)+': </strong><br>'+
                    question.question+
                    '</div>'+
                    '<small class="ml-3">Choices <strong>(Choose '+(question.expected_answers)+')</strong>:</small>'
                )
                .append(function(){
                    let ul = $(document.createElement('ul'))
                    .addClass('list-group list-group-flush');
                    let choices_el;
                    $.each(question.choices,function(i,v){
                        var ch_el = $(document.createElement('a'))
                        .addClass('list-group-item text-dark q-card-choice text-left choice-btn d-flex justify-content-between')
                        .html('<span>'+v.answer+'</span>')
                        .attr({'href':'javascript:void(0)'})
                        .on("click",function(e){set_answer(this,e,v,question)})
                        if(v.my_answer) {
                            ch_el.addClass("bdr-selected");
                        }
                        v.__btn = ch_el;
                        ul.append(ch_el);
                    });
                    return ul;
                })
            );
        }
        return question.__card;
    }
    function render_exam_listview(target){
        containers.main.questionaire.html("");

        containers.main.reviewer.addClass('d-none');
        containers.main.questionaire.removeClass('d-none');

        containers.main.questionaire.removeClass("card-columns");
        
        containers.controls.view_options.removeClass("d-none");
        containers.controls.footer.removeClass("d-none");
        containers.controls.on_finish.removeClass("d-none");
        containers.controls.press_pagination.addClass("d-none");
        containers.controls.point_nav.addClass("d-none");

        alerts.alert_exam_tips.removeClass('d-none');
        alerts.alert_incomplete_exam.addClass('d-none');

        buttons.individual.return_take.addClass('d-none');

        $.each(questions,function(i,question){
            containers.main.questionaire.append(
                render_exam_card(question)
            );
        });

        buttons.individual.return_take.off("click").on("click",render_exam_listview);

        buttons.individual.submit_exam.off("click").on("click",function(e){
            submit_exam(e,true,render_exam_listview);
        });

        if(target instanceof jQuery) scrollToTarget(target);
    }
    function render_exam_pressview(target){
        containers.main.questionaire.html("");
        containers.main.reviewer.addClass('d-none');
        containers.main.questionaire.removeClass('d-none');
        containers.main.questionaire.removeClass("card-columns");

        containers.controls.footer.removeClass("d-none");
        containers.controls.on_finish.removeClass("d-none");
        containers.controls.view_options.removeClass("d-none");
        containers.controls.press_pagination.removeClass("d-none");
        containers.controls.point_nav.removeClass("d-none");

        alerts.alert_exam_tips.removeClass('d-none');
        alerts.alert_incomplete_exam.addClass('d-none');

        let index = 0;
        if(target){
            if(target.attr("data-index")){
                index = parseInt(target.attr("data-index"));
            }else{
                target.attr("data-index",index);
            }
        }

        $.each(questions,function(i,question){
            containers.main.questionaire.append(
                render_exam_card(question)
            );
        });

        containers.main.questionaire.html(render_exam_card(questions[index]));

        let prev = containers.controls.point_nav.find("#press-view-prev");
        let next = containers.controls.point_nav.find("#press-view-next");

        if(questions[index-1]){
            prev.attr("data-index",index-1);
            prev.prop("disabled",false);
        }else{
            prev.prop("disabled",true);
        }

        if(questions[index+1]){
            next.attr("data-index",index+1);
            next.prop("disabled",false);
        }else{
            next.prop("disabled",true);
        }

        render_pressview_pagination(questions[index]);

        buttons.individual.return_take.off("click").on("click",function(){
            $(this).addClass('d-none')
            .attr("data-index",index);
            render_exam_pressview($(this));
        });

        buttons.individual.submit_exam.off("click").on("click",function(e){
            submit_exam(e,true,render_exam_pressview);
        });
    }
    function render_reviewer_tableview(callbackview=function(){alert('none')}){
        containers.main.reviewer.removeClass('d-none');
        containers.main.questionaire.addClass('d-none');
        containers.controls.point_nav.addClass('d-none');
        containers.controls.press_pagination.addClass('d-none');
        containers.controls.view_options.addClass('d-none');

        alerts.alert_exam_tips.addClass('d-none');
        alerts.alert_incomplete_exam.removeClass('d-none');

        let table = $(document.createElement('table')).addClass('table table-sm table-bordered p-0 m-0');
        $.each(questions,function(i,v){
            let answers = 0;
            $.each(v.choices, function(ci,cv){if(cv.my_answer)answers++;});
            let tr = $(document.createElement('tr')).append($(document.createElement('td')).html(i+1));
            tr.append($(document.createElement('td')).attr({'rowspan':((answers==0)?1:answers)}).html(v.question));
            if(answers>0){
                let ma = 0;
                $.each(v.choices, function(ci,cv){
                    let ctd = $(document.createElement('td')).html(cv.answer);
                    if(cv.my_answer){
                        if(ma==0){
                            tr.append(ctd);
                        }else{
                            tr = $(document.createElement('tr'));
                            tr.html(ctd);
                        }
                        table.append(tr);
                        ma++;
                    }  
                });
            }else{
                let ctd = $(document.createElement('td')).html(
                    $(document.createElement('button')).attr({
                        'title':'Click Here to answer',
                        'data-index':i
                    })
                    .addClass('btn btn-light rounded-0 btn-sm')
                    .html("<strong>No Answer</strong>")
                    .on('click',function(){
                        buttons.individual.return_take.addClass('d-none');
                        callbackview($(this));
                    })
                );
                tr.append(ctd);
                table.append(tr);
            }
        });

        containers.main.reviewer_body.html(table);
    }

    function render_pressview_pagination(question){
        let container = containers.controls.press_pagination.find('.pagination');
        container.html("");
        $.each(questions, function(i,v){
            let li = $(document.createElement('li'));
            let anchor = $(document.createElement('button'));

            li.addClass('page-item');
            anchor.addClass('page-link rounded-0')
            .attr({"data-index":i})
            .on("click",function(e){render_exam_pressview($(this));});
            
            let answers = 0;

            $.each(function(ai,av){if(av.my_answer)answers++;});

            if(answers == question.expected_answers){
                li.addClass('border-primary bg-primary');
            }

            if(v==question){
                li.addClass('active');
            }

            container.append(li.html(anchor.html(i+1)));
        });
    }

    function submit_exam(e,interrupt_incomplete=true,callbackview=null){
        let completed = 0;
        let continues = false;
        $.each(questions,function(i,v){if(v.__completed)completed++});
        if(completed>=questions.length){
            continues = true;
        }else{
            if(interrupt_incomplete){
                buttons.individual.return_take.removeClass('d-none');
                buttons.individual.submit_exam.off("click");
                buttons.individual.submit_exam.on("click",function(e){submit_exam(e,false);});
                render_reviewer_tableview(callbackview);
            }else{
                continues = true;
            }
        }
        if(continues){
            $('.choice-btn').off('click');
            xhttp.submit_exam(apply_correctives);
            window.onbeforeunload = function(){return true;}
            submitted = true;
        }
    }

    function switch_to_default_view(){
        buttons.groups.btns_viewm.prop("disabled",false);
        buttons.groups.btns_viewm.removeClass("btn-dark");
        buttons.groups.btns_viewm.addClass("btn-outline-dark");

        $.each(buttons.groups.btns_viewm, function(i,v){
            target = $(v);
            if(target.attr('data-view')==default_view){
                target.prop("disabled",true);
                target.removeClass("btn-outline-dark");
                target.addClass("btn-dark");
            }
        });

        switch (default_view) {
            case 'list':
                render_exam_listview(target);
                break;
            case 'press':
                render_exam_pressview(target);
                break;
            case 'grid':
                break;
        };
    }
    
    function apply_correctives(response){
        let score = 0;
        $.each(response.data,function(i,v){
            $.each(questions, function(iq, vq){
                if(v.id == vq.id){
                    $.each(v.choices,function(ic,vc){
                        if(vc.is_correct_answer){
                            $.each(vq.choices, function(iqc,vqc){
                                if(vqc.id==vc.id){
                                    vqc.is_correct_answer = true;
                                    vqc.reasons = vc.reasons;
                                }
                            });
                        }
                    })
                }
            });
        });
        $.each(questions,function(i,v){
            $.each(v.choices,function(ic,vc){
                vc.__btn.removeClass('bdr-selected');
                if(vc.is_correct_answer && vc.my_answer){
                    let csc = 1/parseFloat(v.expected_answers);
                    score += csc;
                    vc.__btn.addClass('bdr-im_correct')
                    .append('<span><i class="fas fa-check"></i> ( +'+csc+' points!)</span>');
                }
                if(vc.is_correct_answer && !vc.my_answer){
                    vc.__btn.addClass('bdr-correct_answer ch-popover')
                    .append('<span><strong>(Correct Answer)</strong><span>')
                    .attr({
                        'title':'Explanation',
                        'data-toggle':'popover',
                        'data-trigger':'focus',
                        'data-placement':'top',
                        'data-content':(vc.reasons?vc.reasons:'N/A'),
                    })
                    .popover();
                }
                if(!vc.is_correct_answer && vc.my_answer){
                    vc.__btn.addClass('bdr-im_wrong')
                    .append('<span><i class="fas fa-times"></i></span>');
                }
            });
        });
        buttons.individual.submit_exam.hide();
        buttons.individual.return_home.removeClass('d-none');
        buttons.individual.retake_exam.removeClass('d-none');

        alerts.alert_incomplete_exam.addClass('d-none');
        alerts.alert_exam_tips.addClass('d-none');
        alerts.alert_exam_submit_ok.removeClass('d-none');
        alerts.alert_exam_submit_inf.removeClass('d-none');

        containers.summary.exam_summary.removeClass('d-none');
        containers.summary.exam_score.html(score+'/'+questions.length);
        containers.summary.exam_percentage.html(((score/questions.length)*100)+'%');

        scrollToTarget(containers.root);

        switch_to_default_view();
    }
    buttons.individual.start_exam.on("click", function(){
        xhttp.get_questions();
        $(this).addClass('d-none');
        window.onbeforeunload = function(){return 'Are you sure you want to leave?';};
    });
    buttons.individual.backtop.on("click",function(){scrollToTarget(containers.root);})

    buttons.groups.btns_viewm.on("click",function(e){
        let target = $(this);
        let viewmode = $(this).attr('data-view');

        buttons.groups.btns_viewm.prop("disabled",false);
        buttons.groups.btns_viewm.removeClass("btn-dark");
        buttons.groups.btns_viewm.addClass("btn-outline-dark");
        
        target.prop("disabled",true);
        target.removeClass("btn-outline-dark");
        target.addClass("btn-dark");

        switch (viewmode) {
            case 'list':
                render_exam_listview(target);
                break;
            case 'press':
                render_exam_pressview(target);
                break;
            case 'grid':
                break;
        };
    });
    buttons.groups.btns_point_ctrl.on("click",function(e){
        render_exam_pressview($(this));
    });

});