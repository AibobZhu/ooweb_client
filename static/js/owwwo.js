var ootable_timely_execute_queue = []
var ootable_timeout_execute_queue = []

"use strict";

/*
function ooattr(that) {
    var ret = {};
    $.each(that.attributes, function() {
        // this.attributes is not a plain object, but an array
        // of attribute nodes, which contain both the name and value
        if(this.specified) {
            ret[this.name] = this.value
        }
    });
    return ret;
}
*/

function ooweb_base_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if(typeof data != 'undefined' && data != null){
           if($.type(data) == 'object'){
             let that2 = $('#'+that.attr('id'));
             if('style' in data){
               for(var key in data['style']){
                   that2.css(key, data['style'][key]);
               };
             };
             if('attr' in data){
               for(var key in data['attr']){
                   that2.attr(key, data['attr'][key]);
               };
             };
             if('remove_class' in data){
               for(var i in data['remove_class']){
                   that2.removeClass(data['remove_class'][i]);
               }
             };
             if('add_class' in data){
               for(var i in data['add_class']){
                   that2.addClass(data['add_class'][i]);
               };
             };
             if('text' in data){
               that2.text(data['text']);
             };
             if('html' in data){
               that2.html(data['html']);
             };
             if('val' in data){
               that2.val(data['val']);
             };
           };
        }else{
           let styles = oocss(that);
           let attr = that.data();
           let data_attr = {}
           for(var key in attr){
               data_attr['data-'+key] = attr[key];
           };
           let klass = that.prop('className');
           if(typeof(klass) == 'string'){
               klass = klass.split(' ');
           }else{
               klass = '';
           };
           let value = that.val();
           let text = that.text().trim();
           let html = '';
           if (typeof that.html() !== 'undefined'){
               html = that.html().trim();
           };
           var return_value = {'id': that.attr('id'), 'name': that.attr('name')};
           if((return_parts != null)&&(return_parts != 'undefined')){
               if((return_parts.length == 1)&&(return_parts[0] === 'all')){
                   $.extend(return_value, {'style':styles, 'attr': data_attr, 'class':klass, 'val': value, 'text': text, 'html': html});
               }else{
                   if(is_in_list(return_parts, 'style')){
                       $.extend(return_value, {'style': styles});
                   };
                   if(is_in_list(return_parts, 'attr')){
                       $.extend(return_value, {'attr': attr});
                   };
                   if(is_in_list(return_parts, 'class')){
                       $.extend(return_value, {'class': klass});
                   };
                   if(is_in_list(return_parts, 'val')){
                       $.extend(return_value, {'val': value});
                   };
                   if(is_in_list(return_parts, 'text')){
                       $.extend(return_value, {'text': text})
                   };
                   if(is_in_list(return_parts, 'html')){
                       $.extend(return_value, {'html': html})
                   };
               };
           };
           return return_value;
    }
}

function ooweb_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    return ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
}

function var_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if (data == null || data === undefined){
       return that;
    }else{
       that = data;
    }
}

function webbtnradio_on_change(event, that){
    radio = $(that).parent().parent();
    radio.find('input').prop('checked', false);
    radio.find('input').attr('data-checked', false);
    $(that).prop('checked',true);
    $(that).attr('data-checked',true);
}

function webbtnradio_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#'+that.attr('id'));
    if(typeof data != 'undefined' && data != null){
       that2.find('input').each(function(){
           let v = $(this).attr('data-value');
           if(('oovalue' in data && v === data.oovalue) || ('select' in data && v === data.select)){
               that.find('input').prop('checked', false);
               that.find('input').attr('data-checked', false);
               $(this).attr('data-checked', true);
               $(this).prop('checked', true);
               if('oovalue' in data){
                   delete data.oovalue;
               }
               if('select' in data){
                   delete data.select;
               }
           };
       });
       return ooweb_base_val(that=that2, data=data);
    }else{
       let val = null;
       that2.find('input').each(function(){
           let v = $(this).attr('data-checked');
           if(v === 'true'){
               val = $(this).attr('data-value');
           };
       });
       let base_value=ooweb_base_val(that=that2);
       base_value.select = val;
       base_value.oovalue = val;
        if(typeof base_value != 'undefined' && base_value != null){
            base_value.element_type='WebBtnRadio';
        };
       return base_value;
    };
}

function webcomponent_draw_img(img, height){
    $(img).jqthumb({
       classname: "jqthumb",
       width : "100%",
       height : height,
       position : {y: "50%", x: "50%"},
       zoom : "1",
       method : "auto"
    });
}

function webdiv_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebDiv';
    };
    return ret;
}

function webrow_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebRow';
    };
    return ret;
}

function webcolumn_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebColumn';
    };
    return ret;
}

function webhead1_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHead1';
    };
    return ret;
}

function webhead2_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHead2';
    };
    return ret;
}

function webhead3_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHead3';
    };
    return ret;
}

function webhead4_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHead4';
    };
    return ret;
}

function webhead5_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHead5';
    };
    return ret;
}

function webhead6_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHead6';
    };
    return ret;
}

function webfield_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#' + that.attr('id'));
    if(typeof data != 'undefined' && data != null){
       if('val' in data){
           that2.find('legend').text(data['val']);
       };
       delete data['val'];
       if('text' in data){
           delete data['text'];
       };
    };
    ret = ooweb_base_val(that=that2, data=data);
    if(typeof data == 'undefined' || data == null){
       ret['textfield_text'] = that2.find('legend').text();
    };
    if(typeof ret !== 'undefined' && ret !== null){
        ret.element_type = 'WebField';
    };
    return ret;
}

function webi_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebI';
    };
    return ret;
}

function webimg_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#' + that.attr('id'));
    if(typeof data != 'undefined' && data != null){
       if($.type(data) == 'object'){
           if('oovalue' in data){
               if('attr' in data){
                   data.attr.src = data.oovalue;
               }else{
                   data = {'attr':{'src':data.oovalue}};
               }
           }
           if('value' in data){
               if('attr' in data){
                   data.attr.src = data.value;
               }else{
                   data = {'attr':{'src': data.value}};
               }
           }
       }
       ooweb_base_val(that=that2, data=data, trigger_event=trigger_event, return_parts=return_parts);
    }else{
        let ret = ooweb_base_val(that=that2, data=data);
        if(typeof ret != 'undefined' && ret != null){
            ret.element_type='WebImg';
        };
        return ret;
    }
}

function webb_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebB';
    };
    return ret;
}

function webhr_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebHr';
    };
    return ret;
}

function webbtn_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#' + that.attr('id'));
    if (data == null || data === undefined){
        let ret = ooweb_base_val(that=that2);
        if(typeof ret != 'undefined' && ret != null){
            ret.element_type='WebBtn';
        };
        return ret;
    }else{
       if(typeof(data) === 'object'){
           if('oovalue' in data){
               that2.text(data.oovalue);
               if('text' in data){
                   delete data.text;
               };
               if('val' in data){
                   delete data.val;
               };
               if('value' in data){
                   delete data.value;
               };
           }
           if('value' in data){
               that2.text(data.value);
               if('text' in data){
                   delete data.text;
               };
               if('val' in data){
                   delete data.val;
               };
               if('oovalue' in data){
                   delete data.oovalue;
               };
           }
           if('text' in data){
               that2.text(data.text);
               delete data.text;
               if('val' in data){
                   delete data.val;
               }
               if('value' in data){
                   delete data.value;
               };
           }
           if('val' in data){
               that2.text(data.val);
               delete data.val;
               if('value' in data){
                   delete data.value;
               };
           }
           if('value' in data){
               that2.text(data.value);
               delete data.value;
           };
           ooweb_base_val(that=that2, data=data);
       }else{
           that2.text(data);
       }
       that2.change();
    };
}

function webbtntoggle_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = webbtn_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type='WebBtnToggle';
    };
    return ret;
}

function webselect_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if(typeof data != 'undefined' && data != null){
       that = $('#'+String(that.attr('id')));
       if('options' in data){
           that.empty();
           for(var i=0, len=data['options'].length; i<len; i++){
               let option = data['options'][i];
               if('option_group' in option){
                   that.append('<optgroup label=\"' + option['label'] + '\"');
               }else{
                   let optstr = '<option ';
                   if('value' in option){
                       optstr = optstr + ' value=\"'+option['value'] + '\"';
                   };
                   if(('selected' in option) && (option['selected'] === 'true' || option['selected'] === true)){
                       optstr = optstr + ' selected ';
                   };
                   if('attr' in option){
                       for(var a in option['attr']){
                           optstr = optstr + ' ' + a + '=' + option['attr'][a] + ' ';
                       }
                   };
                   if('style' in option){
                       optstr = optstr + ' style=\"';
                       for(var s in option['style']){
                           optstr = optstr + s + ':' + option['style'][s] + ';';
                       };
                       optstr = optstr + '\" '
                   };
                   if('classes' in option){
                       optstr = optstr + ' class=\"'
                       for(var ci =0, len = option['classes'].length; ci < len; ci++){
                           optstr = optstr + option['classes'][ci] + ' ';
                       };
                       optstr = optstr + '\" ';
                   };
                   optstr = optstr + '>'
                   if('text' in option){
                       optstr = optstr + option['text'];
                   };
                   that.append(optstr + '</option>');
               };
           }
       };
       ooweb_base_val(that, data);
    }else{
       let val = ooweb_base_val(that=that);
       val['selected'] = that.find(':selected').text().trim();
       val.element_type='WebSelect';
       return val;
    }
}

function webdatalist_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = webselect_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebDatalist';
    };
    return ret;
}

function webspan_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebSpan';
    };
    return ret;
}

function weba_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebA';
    };
    return ret;
}

function webli_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebLi';
    };
    return ret;
}

function webul_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#'+String(that.attr('id')));
    if(typeof data != 'undefined' && data != null){
       let lis = that2.find('li');
       if('oovalue' in data){
           that2.text(data.oovalue);
           if('text' in data){
               delete data.text;
           }
           that2.append(lis);
       }
       if('text' in data){
           that2.text(data.text);
           delete data.text;
           that2.append(lis);
       }
       ooweb_base_val(that=that2, data=data, trigger_event=trigger_event, return_parts=return_parts);
    }else{
        let ret = ooweb_base_val(that=that2);
        if(typeof ret != 'undefined' && ret != null){
            ret.element_type='WebUl';
        };
        return ret;
    }
}

function webinput_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebInput';
    };
    return ret;
}

function weblabel_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'WebLabel';
    };
    return ret;
}

function webcheckbox_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if(typeof data != 'undefined' && data != null){
       if($.type(data) == 'object'){let that_ = $('#'+that.attr('id'));
         if('checked' in data){
            if(data.checked){
               that.find('input').prop('checked',true);
            }else{
               that.find('input').prop('checked',false);
            };
         };
         if('text' in data){
           let label = that_.find('label');
           label.text(data.text);
           delete data.text;
         };
         if('html' in data){
           delete data.html;
         };
         if('val' in data){
           delete data.val;
         };
       };
       ooweb_base_val(that=that, data=data);
    }else{
       ret = ooweb_base_val(that=that);
       ret['checked'] = that.find('input').prop('checked');
       let label = that.find('label');
       ret['label'] = label.text().trim();
       ret.element_type = 'WebCheckbox';
       return ret;
    }
}

function webbtndd_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#' + String(that.attr('id')));
    if (data == null || data === undefined){
       let ret = {};
       ret['text'] = that2.text().trim();
       ret.element_type = 'WebBtnDropdown';
       return ret;
    }else{
       let span = $(that2.find('span')[0]);
       if(data.hasOwnProperty('select')){
           that2.text(data.select);
       }else if ((data.hasOwnProperty('text') || (data.hasOwnProperty('name')))){
           that2.text(data.text);
       };
       if(data.hasOwnProperty('options') && data.options instanceof Array ){
           webbtndd_set_options(that2, data.options);
       };
       if(typeof(data) == 'string'){
           that2.text(data);
       };
       that2.append(span);
       that2.change();
    };
}

function webbtngrp_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#' + that.attr('id'));
    if (data == null || typeof data == 'undefined'){
        let children_values = Array();
        that2.children().each(function(){
            if($(this).find('input').length==1){
               children_values.push(webcheckbox_val(that=$(this), data=null));
            };
            if($(this).is('button')){
               children_values.push(webbtn_val(that=$(this), data=null));
            };
        });
        let ret = {};
        ret.children = children_values;
        ret.element_type = 'WebBtnGroup';
        ret.me = that2.prop('name');
        return ret;
    }else{
        let ret = ooweb_base_val(that=that2, data=data, trigger_event=trigger_event, return_parts=return_parts);
        if(typeof ret != 'undefined' && ret != null){
            ret.element_type='WebBtnGroup';
        };
        return ret;
    };
}

function oogeneral_selector_val_by_btn(btn_id){
    var $gselector = $($("#"+btn_id).parent().parent());
    var ret = [];
    $gselector.find("button").each(function(i,v){
           ret.push($(v).text().trim());
       }
    )
    return ret;
}

function oogeneral_selector_btn_change($btn, $gs){
    var found = false;
    $gs.find('button').each(function(index,e){
       if($btn.attr('id') == $(e).parent().attr('id')){
           found = true;
       }else if(found){
           let $span = $(e).find('span');
           $(e).text($(e).data('value'));
           $(e).append($span);
       };
    });
}

function oogselector_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if((typeof data != 'undefined') && (data instanceof Array) && (data != null)){
       for(let i in data){
           let value = data[i];
           let text = '';
           if(value.hasOwnProperty('select') && value.select != '' && value.select != null ){
               text = value.select;
           }else{
               text = value.name;
           };
           let btn_grp = $(that.children()[i]);
           let btn = $(btn_grp.find('button')[0]);
           let span = $(btn_grp.find('span')[0]);
           btn.text(text);
           btn.append(span);
           if(value.hasOwnProperty('options') && value.options instanceof Array ){
               let ul = $(btn_grp.children('ul')[0]);
               ul.empty();
               if(value.options.length >0 ){
                   value.options.forEach(function(val){
                       ul.append('<li><a>' + val.name + '</a></li>');
                   });
                   btn.removeAttr('disabled');
               }else{
                   btn.attr('disabled','disabled');
               };
           };
       };
       if(trigger_event){
           that.change();
       };
    }else{
       var ret = [];
       that.children().each(function(){
           let btn = $(this).find('button');
           let options = [];
           let ul = $(this).find('ul');
           ul.find('a').each(function(){
               options.push({'name':$(this).text().trim(),'href':$(this).attr('href')});
           });
           ret.push({'select':btn.text().trim(),'name':btn.attr('data-value'),'options':options});
       });
       ret.element_type = 'OOGeneralSelector';
       return ret;
    };
}

function oogselector_render(that, url){
    let data = {'data':oogselector_val(that), 'me':that.name()};
    let data_j = JSON.stringify(data);
    $.post(url, {'data':data_j}, function(response,status){
        if (status == 'success'){
            let data = response.data;
            oogselector_val(that, data, false);
        };
    });
}

function oodatepickersimple_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'OODatePickerSimple';
    };
    return ret;
}

function oodatepickericon_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'OODatePickerIcon';
    };
    return ret;
}

function oodatepickerrange_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'OODatePickerRange';
    };
    return ret;
}

function oobanner_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let ret = ooweb_base_val(that=that, data=data, trigger_event=trigger_event, return_parts=return_parts);
    if(typeof ret != 'undefined' && ret != null){
       ret.element_type = 'OOBanner';
    };
    return ret;
}

function oocalendar_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let calendar = that.data('calendar');
    if (data == null){
       let view = calendar.options.view;
       let title = calendar.getTitle();
       let start = calendar.options.position.start.getTime();
       let end = calendar.options.position.end.getTime();
       let ret = {};
       ret.element_type='OOCalendar';
       ret.start=start;
       ret.end=end;
       ret.title=title;
       ret.view=view;
       return ret;
    }else{
       let data_ = data;
       let view_ = data_.view;
       let hierarchy_ = data_.hierarchy;
       oocalendar_chane_event_trigger = false;
       calendar.update_events(extra_data=hierarchy_);
       oocalendar_chane_event_trigger = true;
    }
}

function webtab_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if(typeof data != 'undefined' && data != null){
        if('active_tab' in data){
            that.find('li').removeClass('active');
            that.find('[data-value=\"'+data.active_tab+'\"]').parent().addClass('active');
            that.find('[data-toggle=\"tab\"]').attr('aria_expanded', 'false');
            that.find('[data-value=\"'+data.active_tab+'\"]').attr('aria_expanded','true');
        }
    }else{
       let val = that.find('.active').text().trim();
       let ret = {};
       ret.active_tab=val;
       ret.element_type='WebTab';
       return ret;
    }
}

function webtabcontain_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let that2 = $('#'+that.prop('id'));
    if(typeof data != 'undefined' && data != null){
        if('active_tab' in data){
            that2.find('.tab-pane').removeClass('active');
            that2.find('.tab-pane').removeClass('in');
            $('#'+data.active_tab).addClass('active');
            $('#'+data.active_tab).addClass('in');
        };
    }else{
       let val = that2.find('.active').attr('id');
       let ret = {};
       ret.active_tab=val;
       ret.element_type='WebTabContain';
       return ret;
    }
}

function webtable_render(id, data){
    $('#'+id).empty();
    $('#'+id).append(data.html);
}

function webtable_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let id = that.attr('id');
    if((data === null)||(typeof data == 'undefined')){
        return null;
    };
    return webtable_render(id,data=data);
}
const OOTABLE_RENDER_IMG_KEY = 'ootable_render_img'
const OOTABLE_RENDER_CHART_KEY = 'ootable_chart_img'

function ootable_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    if(data == null || data === undefined || !('setting' in data)){
        return {'value':ooweb_base_val(that),'element_type':'OOTable'};
    };
    let setting = data.setting;
    if(that.children().length != 0){
       that.DataTable().clear();
       that.DataTable().destroy();
       that.empty();
    };
    that.append(data.html);
    if('columnDefs' in setting){
       setting.columnDefs.push({'targets':'_all','data':undefined, 'render':ootable_cell_render, createdCell:ootable_created_cell_render});
    }else{
       setting.columnDefs = [{"targets":"_all","data":undefined,"render":ootable_cell_render, createdCell:ootable_created_cell_render}];
    };
    let table = that.DataTable(setting);
    that.on('expand-row.bs.table', function (e,index, row, $detail){
                                       alert(JSON.stringify(row));
                                   });
    table.draw();
    if(data.html.includes(OOTABLE_RENDER_IMG_KEY) || data.html.includes(OOTABLE_RENDER_CHART_KEY)){
       let tr_num = data.html.split('<tr').length - 1;
       let seconds = tr_num * 230;
       setTimeout(function(){
           that.DataTable().draw();
           that.trigger('draw_done');
       }.bind(that,data),seconds);
    }else{
       that.trigger('draw_done');
    };
    delete data['html'];
    ooweb_base_val(that, data);
}

function ootaggroup_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    let data_={};
    if(data === null){
       data_ = {'html':null,'checked':'checked', 'tags':false};
    }else{
       data_ = data;
    };
    let html = data_.html;
    var id = that.attr('id');
    var that2 = $('#'+String(id));
    if(html){
        that2.empty();
        that2.html(html);
    };
    let checked = data_.checked;
    if(checked === undefined || checked === null){
        return;
    };
    let tags = data_.tags;
    if (checked === "checked"){
        if(!tags){
            var checked_values = [];
            $("#"+id+" :checked").each(function(){
                let label = $.trim($(this).parent().parent().find('label').text())
                checked_values.push(label);
            });
            checked_values = checked_values.join(" ");
            let ret = {}
            ret.checked_values = checked_values
            ret.me = that2.prop('name')
            ret.element_type = 'OOTagGroup'
            return ret
        }else{
            ;
        };
    }else if(checked === "unchecked"){
        if(!tags){
            var unchecked_values = [];
            $("#"+id+" :unchecked").each(function(){
                let label = $.trim($(this).parent().parent().find('label').text())
                unchecked_values.push(label);
            });
            unchecked_values = unchecked_values.join(" ");
            let ret = {}
            ret.unchecked_values = unchecked_values
            ret.me = that2.prop('name')
            ret.element_type = 'OOTagGroup'
            return ret
        }else{
            ;
        };
    }else if(checked === true){
        that2.find('input').prop('checked',true);
    }else if(checked === false){
        that2.find('input').prop('checked',false);
    }else if(checked instanceof Array){
       that2.find('input').prop('checked',false);
       let length = checked.length;
       for(let i=0;i<length;i++){
           let search = 'label:contains(' + checked[i] + ')';
           let label = $(search);
           let parent = label.parent();
           let input = parent.find('input');
           input.prop('checked',true);
       };
    };
}

const OOCHAT_BODY = 'oochat_body_'
const OOCHAT_SEND_INPUT = 'oochat_send_input_'
const OOCHAT_SEND_BTN = 'oochat_send_btn_'

function oochat_message(data, me){
    let klass='';
    let styles='';
    let room='';
    let who='';
    if(data['to']===me){
       klass='pull-left';
       styles={'background-colour': '#f4429b'};
       room=me;
       who=data['from'];
    }else if(data['from']===me){
       klass='pull-right';
       styles={'background-color': '#f7f7d6'};
       room=me;
       who=data['from'];
    }else{
       return;
    };
    $room = $('.panel-body');
    $room.append('<div class=\"clearfix\" style=\"\"><blockquote class=\"'+klass+'\" style=\"'+styles+'\"><b>'+who+':</b>'+data['message']+'</blockquote></div>');
}

function oochatclient_val(that, data=null, trigger_event=false, return_parts=["val","text"]){

    let body_name = OOCHAT_BODY + that.prop('name')
    let body_id = body_name
    let send_input_name = OOCHART_SEND_INPUT + that.prop('name')
    let send_input_id = send_input_name
    let send_btn_name = OOCHART_SEND_BTN + that.prop('name')
    let send_btn_id = send_btn_name

    if(typeof data != 'undefined' && data != null){
       var datai = null;
       for(var i=0, len=data.length; i<len; i++){
           datai = data[i];
           if((datai !== null)&&(typeof datai !== 'undefined')){
               if(datai['me']==body_name){
                   webdiv_val(that=$('#'+body_id), data=datai['data']);
               }else if(datai['me']==send_input_name){
                   webinput_val(that=$('#'+send_input_id), data=datai['data']);
               }else if(datai['me']==send_btn_name){
                   webbtn_val(that=$('#'+body_id), data=datai['data']);
               };
           };
       };
    }else{
       let val = [ {
                       'me':body_name, 'data':webdiv_val(that=$('#'+body_id)), 'element_type':'oochatclient_body'
                   },
                   {
                       'me':send_input_name, 'data':webinput_val(that=$('#'+send_input_id)), 'element_type':'oochatclient_input'
                   },
                   {
                       'me':send_btn_name, 'data':webbtn_val(that=$('#'+send_btn_id)), 'element_type':'oochatclient_btn'
                   }
                 ];
       return val;
    };
}

function oochatserver_val(that, data=null, trigger_event=false, return_parts=["val","text"]){
    ;
}

function is_in_list(list, element) {
    for(var i=0;i<list.length;i++){
        if(element === list[i]){
            return true;
        }
    }
    return false;
}

function oocss(a) {
    var sheets = document.styleSheets, o = {};
    for (var i in sheets) {
        var rules = sheets[i].rules || sheets[i].cssRules;
        for (var r in rules) {

            if(typeof rules[r].selectorText !== 'undefined'){
                if(rules[r].selectorText.indexOf('a:hover')>=0){
                    //o = $.extend(o, oocss2json(rules[r].style), oocss2json(a.attr('style')));
                } else if (rules[r].selectorText.indexOf('-moz-focus-inner')>=0){
                    //o = $.extend(o, oocss2json(rules[r].style), oocss2json(a.attr('style')));
                } else if (rules[r].selectorText.indexOf('webkit-outer-spin-button')){
                    //o = $.extend(o, oocss2json(rules[r].style), oocss2json(a.attr('style')));
                } else if (a.is(rules[r].selectorText)) {
                    o = $.extend(o, oocss2json(rules[r].style), oocss2json(a.attr('style')));
                }
            }
        }
    }
    return o;
}

function oocss2json(css) {
    var s = {};
    if (!css) return s;
    if (css instanceof CSSStyleDeclaration) {
        for (var i in css) {
            if ((css[i]).toLowerCase) {
                s[(css[i]).toLowerCase()] = (css[css[i]]);
            }
        }
    } else if (typeof css == "string") {
        css = css.split("; ");
        for (var i in css) {
            var l = css[i].split(": ");
            s[l[0].toLowerCase()] = (l[1]);
        }
    }
    return s;
}

function oocalendar_start(options=null){
    var opts_default = {
            id: 'oocalendar',
            events_source: '/OOCalendar.test',
            view: 'month',
            tmpl_path: '/OOCalendar.test',
            tmpl_cache: false,
            day: '2013-03-12',
            onAfterEventsLoad: function(events) {
                if(!events) {
                    return;
                }
                var list = $('#eventlist');
                list.html('');

                $.each(events, function(key, val) {
                    $(document.createElement('li'))
                        .html('<a href="' + val.url + '">' + val.title + '</a>')
                        .appendTo(list);
                });
            },
            onAfterViewLoad: function(view) {
                $('.page-header h3').text(this.getTitle());
                $('.btn-group button').removeClass('active');
                $('button[data-calendar-view="' + view + '"]').addClass('active');
            },
            classes: {
                months: {
                    general: 'label'
                }
            },
            language: 'zh-TW'
        };

    var opts= opts_default
    if((options != null) && (options !== 'undefined')){
        for(var key in opts){
            if(opts.hasOwnProperty(key)){
                if(options.hasOwnProperty(key)){
                    opts[key] = options[key]
                }
            }
        }
    }
    var that = $('#'+opts.id);
	var calendar_ = that.calendar(opts);
	var calendar = that.data('calendar');
    calendar.setOptions({first_day: 1});
    calendar.setLanguage(opts.language);
    calendar.view();

    /*
    $.ajax({
        url: options.tmpl_path + '\oocalendar-bar.html',
        dataType: 'html',
        type: 'GET',
        async: false,
        cache: true
	}).done(function(html) {
		$('#oocalendar-bar').append(html)
	});
    */

    $('.btn-group button[data-calendar-nav]').each(function() {
            var $this = $(this);
            $this.click(function() {
                calendar.navigate($this.data('calendar-nav'));
                that.change();
            });
	    });

    $('.btn-group button[data-calendar-view]').each(function() {
        var $this = $(this);
        $this.click(function() {
            calendar.view($this.data('calendar-view'));
            that.change();
        });
    });

    $('#language').change(function(){
        calendar.setLanguage($(this).val());
        calendar.view();
    });

    $('#events-in-modal').change(function(){
        var val = $(this).is(':checked') ? $(this).val() : null;
        calendar.setOptions({modal: val});
    });
    $('#format-12-hours').change(function(){
        var val = $(this).is(':checked') ? true : false;
        calendar.setOptions({format12: val});
        calendar.view();
    });
    $('#show_wbn').change(function(){
        var val = $(this).is(':checked') ? true : false;
        calendar.setOptions({display_week_numbers: val});
        calendar.view();
    });
    $('#show_wb').change(function(){
        var val = $(this).is(':checked') ? true : false;
        calendar.setOptions({weekbox: val});
        calendar.view();
    });

	$('#events-modal .modal-header, #events-modal .modal-footer').click(function(e){
		//e.preventDefault();
		//e.stopPropagation();
	});
};

$(function(){
    setInterval(function(){
        $.each(ootable_timely_execute_queue, function(index, value){
          value();
        });
    },3000);
    setTimeout(function(){
        $.each(ootable_timeout_execute_queue, function(index, value){
            value();
        })
    },10000);
});

function ootable_init_complete() {
    this.api().columns.adjust().draw()
};

function ootable_get_row_data(that, data_attr="ootable-details"){
    let row_that = that[0];
    let that_ = that[1];
    if(!that_){
       var tds = $(row_that).children();
       var ret = [];
       tds.each(function(index, element){
           let klass = $(element).attr("class");
           let style = $(element).attr("style");
           let data = $(element).data(data_attr);
           ret.push({'class':klass, 'style':style, 'data':data});
       });
       return ret;
    }else{
       ootable_val(that_,data_attr);
    };
}

$.attrHooks['viewbox'] = {
    set: function(elem, value, name) {
        elem.setAttributeNS(null, 'viewBox', value + '');
        return value;
    }
};

function stream_layers(n, m, o) {
  if (arguments.length < 3) o = 0;
  function bump(a) {
    var x = 1 / (.1 + Math.random()),
        y = 2 * Math.random() - .5,
        z = 10 / (.1 + Math.random());
    for (var i = 0; i < m; i++) {
      var w = (i / m - y) * z;
      a[i] += x * Math.exp(-w * w);
    }
  }
  return d3.range(n).map(function() {
      var a = [], i;
      for (i = 0; i < m; i++) a[i] = o + o * Math.random();
      for (i = 0; i < 5; i++) bump(a);
      return a.map(stream_index);
    });
}

/* Another layer generator using gamma distributions. */
function stream_waves(n, m) {
  return d3.range(n).map(function(i) {
    return d3.range(m).map(function(j) {
        var x = 20 * j / m - i / 3;
        return 2 * x * Math.exp(-.5 * x);
      }).map(stream_index);
    });
}

function stream_index(d, i) {
  return {x: i, y: Math.max(0, d)};
}

function oochart_create_svg(svg_id, svg=null){
    let svg_d3 = null;
    if(svg_id == null && svg != null){
        svg_d3 = d3.select(svg);
    }else if(svg_id != null && svg == null){
        $('#'+svg_id).empty();
        svg_d3 = d3.select('#'+svg_id);
    }else{
        console.assert(false, 'Both svg_id and svg are null, only one of them should be valid.');
    }
    return svg_d3
}

function oochart_linefinder_example_data(){
    return stream_layers(3,10+Math.random()*200,.1).map(function(data, i) {
        return {
          key: 'Stream' + i,
          values: data
        };
    });
};
function oochart_linefinder_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
  var svg_d3 = oochart_create_svg(svg_id,svg);

  nv.addGraph(function() {
      var chart = nv.models.lineWithFocusChart();
        if(simple){
            chart.showLegend(false).showXAxis(false).showYAxis(false);
        };
      chart.xAxis
        .tickFormat(d3.format(',f'));

      chart.yAxis
        .tickFormat(d3.format(',.2f'));

      chart.y2Axis
        .tickFormat(d3.format(',.2f'));

      if((typeof data) == 'string'){
        data = oochart_example_datas[data]();
      };

      svg_d3.datum(data)
        .transition().duration(duration)
        .call(chart)
        ;

      nv.utils.windowResize(chart.update);

      return chart;
    });

}

function oochart_bullet_example_data(){
    return {
      "title": "Revenue",
      "subtitle": "US$, in thousands",
      "ranges": [150,225,300],
      "measures": [220],
      "markers": [250]
    }
}
function oochart_bullet_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
        var chart = nv.models.bulletChart();
        svg_d3.datum(data)
            .transition().duration(duration)
            .call(chart)
            ;
        return chart;
    },function(){
        if(simple){
            let title = svg_d3.selectAll('.nv-titles');
            title.attr('display','none');
            let tick = svg_d3.selectAll('.nv-tick');
            tick.attr('display','none');
        };
    });

}

function oochart_pie_example_data(){
     return [
          {
            "label": "One",
            "value" : 29.765957771107
          } ,
          {
            "label": "Two",
            "value" : 0
          } ,
          {
            "label": "Three",
            "value" : 32.807804682612
          } ,
          {
            "label": "Four",
            "value" : 196.45946739256
          } ,
          {
            "label": "Five",
            "value" : 0.19434030906893
          } ,
          {
            "label": "Six",
            "value" : 98.079782601442
          } ,
          {
            "label": "Seven",
            "value" : 13.925743130903
          } ,
          {
            "label": "Eight",
            "value" : 5.1387322875705
          }
    ]

}
function oochart_pie_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
  var svg_d3 = oochart_create_svg(svg_id,svg);
  nv.addGraph(function() {
      var chart = nv.models.pieChart()
          .x(function(d) { return d.label })
          .y(function(d) { return d.value })
          .showLabels(true);
      if(simple){
        //chart.margin({top:0,right:0,bottom:0,left:0});
        chart.showLegend(false).showLabels(false).legend.margin({top:0,right:0,bottom:0,left:0});
      }
        svg_d3.datum(data)
          .transition().duration(duration)
            .call(chart);

      return chart;
  },function(){
    if(simple){
       svg_d3.selectAll('.nv-legend').remove();
       svg_d3.selectAll('text').remove();
       svg_d3.selectAll('.nv-legendWrap').remove();
       svg_d3.selectAll('.nv-pieLabels').remove();

    };
  });

}

function oochart_cumulativeline_example_data(){
    return [
      {
        "key": "Series 1",
        "values": [ [ 1025409600000 , 0] , [ 1028088000000 , -6.3382185140371] , [ 1030766400000 , -5.9507873460847] , [ 1033358400000 , -11.569146943813] , [ 1036040400000 , -5.4767332317425] , [ 1038632400000 , 0.50794682203014] , [ 1041310800000 , -5.5310285460542] , [ 1043989200000 , -5.7838296963382] , [ 1046408400000 , -7.3249341615649] , [ 1049086800000 , -6.7078630712489] , [ 1051675200000 , 0.44227126150934] , [ 1054353600000 , 7.2481659343222] , [ 1056945600000 , 9.2512381306992] , [ 1059624000000 , 11.341210982529] , [ 1062302400000 , 14.734820409020] , [ 1064894400000 , 12.387148007542] , [ 1067576400000 , 18.436471461827] , [ 1070168400000 , 19.830742266977] , [ 1072846800000 , 22.643205829887] , [ 1075525200000 , 26.743156781239] , [ 1078030800000 , 29.597478802228] , [ 1080709200000 , 30.831697585341] , [ 1083297600000 , 28.054068024708] , [ 1085976000000 , 29.294079423832] , [ 1088568000000 , 30.269264061274] , [ 1091246400000 , 24.934526898906] , [ 1093924800000 , 24.265982759406] , [ 1096516800000 , 27.217794897473] , [ 1099195200000 , 30.802601992077] , [ 1101790800000 , 36.331003758254] , [ 1104469200000 , 43.142498700060] , [ 1107147600000 , 40.558263931958] , [ 1109566800000 , 42.543622385800] , [ 1112245200000 , 41.683584710331] , [ 1114833600000 , 36.375367302328] , [ 1117512000000 , 40.719688980730] , [ 1120104000000 , 43.897963036919] , [ 1122782400000 , 49.797033975368] , [ 1125460800000 , 47.085993935989] , [ 1128052800000 , 46.601972859745] , [ 1130734800000 , 41.567784572762] , [ 1133326800000 , 47.296923737245] , [ 1136005200000 , 47.642969612080] , [ 1138683600000 , 50.781515820954] , [ 1141102800000 , 52.600229204305] , [ 1143781200000 , 55.599684490628] , [ 1146369600000 , 57.920388436633] , [ 1149048000000 , 53.503593218971] , [ 1151640000000 , 53.522973979964] , [ 1154318400000 , 49.846822298548] , [ 1156996800000 , 54.721341614650] , [ 1159588800000 , 58.186236223191] , [ 1162270800000 , 63.908065540997] , [ 1164862800000 , 69.767285129367] , [ 1167541200000 , 72.534013373592] , [ 1170219600000 , 77.991819436573] , [ 1172638800000 , 78.143584404990] , [ 1175313600000 , 83.702398665233] , [ 1177905600000 , 91.140859312418] , [ 1180584000000 , 98.590960607028] , [ 1183176000000 , 96.245634754228] , [ 1185854400000 , 92.326364432615] , [ 1188532800000 , 97.068765332230] , [ 1191124800000 , 105.81025556260] , [ 1193803200000 , 114.38348777791] , [ 1196398800000 , 103.59604949810] , [ 1199077200000 , 101.72488429307] , [ 1201755600000 , 89.840147735028] , [ 1204261200000 , 86.963597532664] , [ 1206936000000 , 84.075505208491] , [ 1209528000000 , 93.170105645831] , [ 1212206400000 , 103.62838083121] , [ 1214798400000 , 87.458241365091] , [ 1217476800000 , 85.808374141319] , [ 1220155200000 , 93.158054469193] , [ 1222747200000 , 65.973252382360] , [ 1225425600000 , 44.580686638224] , [ 1228021200000 , 36.418977140128] , [ 1230699600000 , 38.727678144761] , [ 1233378000000 , 36.692674173387] , [ 1235797200000 , 30.033022809480] , [ 1238472000000 , 36.707532162718] , [ 1241064000000 , 52.191457688389] , [ 1243742400000 , 56.357883979735] , [ 1246334400000 , 57.629002180305] , [ 1249012800000 , 66.650985790166] , [ 1251691200000 , 70.839243432186] , [ 1254283200000 , 78.731998491499] , [ 1256961600000 , 72.375528540349] , [ 1259557200000 , 81.738387881630] , [ 1262235600000 , 87.539792394232] , [ 1264914000000 , 84.320762662273] , [ 1267333200000 , 90.621278391889] , [ 1270008000000 , 102.47144881651] , [ 1272600000000 , 102.79320353429] , [ 1275278400000 , 90.529736050479] , [ 1277870400000 , 76.580859994531] , [ 1280548800000 , 86.548979376972] , [ 1283227200000 , 81.879653334089] , [ 1285819200000 , 101.72550015956] , [ 1288497600000 , 107.97964852260] , [ 1291093200000 , 106.16240630785] , [ 1293771600000 , 114.84268599533] , [ 1296450000000 , 121.60793322282] , [ 1298869200000 , 133.41437346605] , [ 1301544000000 , 125.46646042904] , [ 1304136000000 , 129.76784954301] , [ 1306814400000 , 128.15798861044] , [ 1309406400000 , 121.92388706072] , [ 1312084800000 , 116.70036100870] , [ 1314763200000 , 88.367701837033] , [ 1317355200000 , 59.159665765725] , [ 1320033600000 , 79.793568139753] , [ 1322629200000 , 75.903834028417] , [ 1325307600000 , 72.704218209157] , [ 1327986000000 , 84.936990804097] , [ 1330491600000 , 93.388148670744]]
      },
      {
        "key": "Series 2",
        "values": [ [ 1025409600000 , 0] , [ 1028088000000 , 0] , [ 1030766400000 , 0] , [ 1033358400000 , 0] , [ 1036040400000 , 0] , [ 1038632400000 , 0] , [ 1041310800000 , 0] , [ 1043989200000 , 0] , [ 1046408400000 , 0] , [ 1049086800000 , 0] , [ 1051675200000 , 0] , [ 1054353600000 , 0] , [ 1056945600000 , 0] , [ 1059624000000 , 0] , [ 1062302400000 , 0] , [ 1064894400000 , 0] , [ 1067576400000 , 0] , [ 1070168400000 , 0] , [ 1072846800000 , 0] , [ 1075525200000 , -0.049184266875945] , [ 1078030800000 , -0.10757569491991] , [ 1080709200000 , -0.075601531307242] , [ 1083297600000 , -0.061245277988149] , [ 1085976000000 , -0.068227316401169] , [ 1088568000000 , -0.11242758058502] , [ 1091246400000 , -0.074848439408270] , [ 1093924800000 , -0.11465623676497] , [ 1096516800000 , -0.24370633342416] , [ 1099195200000 , -0.21523268478893] , [ 1101790800000 , -0.37859370911822] , [ 1104469200000 , -0.41932884345151] , [ 1107147600000 , -0.45393735984802] , [ 1109566800000 , -0.50868179522598] , [ 1112245200000 , -0.48164396881207] , [ 1114833600000 , -0.41605962887194] , [ 1117512000000 , -0.48490348490240] , [ 1120104000000 , -0.55071036101311] , [ 1122782400000 , -0.67489170505394] , [ 1125460800000 , -0.74978070939342] , [ 1128052800000 , -0.86395050745343] , [ 1130734800000 , -0.78524898506764] , [ 1133326800000 , -0.99800440950854] , [ 1136005200000 , -1.1177951153878] , [ 1138683600000 , -1.4119975432964] , [ 1141102800000 , -1.2409959736465] , [ 1143781200000 , -1.3088936375431] , [ 1146369600000 , -1.5495785469683] , [ 1149048000000 , -1.1563414981293] , [ 1151640000000 , -0.87192471725994] , [ 1154318400000 , -0.84073995183442] , [ 1156996800000 , -0.88761892867370] , [ 1159588800000 , -0.81748513917485] , [ 1162270800000 , -1.2874081041274] , [ 1164862800000 , -1.9234702981339] , [ 1167541200000 , -1.8377768147648] , [ 1170219600000 , -2.7107654031830] , [ 1172638800000 , -2.6493268125418] , [ 1175313600000 , -3.0814553134551] , [ 1177905600000 , -3.8509837783574] , [ 1180584000000 , -5.2919167850718] , [ 1183176000000 , -5.2297750650773] , [ 1185854400000 , -3.9335668501451] , [ 1188532800000 , -2.3695525190114] , [ 1191124800000 , -2.3084243151854] , [ 1193803200000 , -3.0753680726738] , [ 1196398800000 , -2.2346609938962] , [ 1199077200000 , -3.0598810361615] , [ 1201755600000 , -1.8410154270386] , [ 1204261200000 , -1.6479442038620] , [ 1206936000000 , -1.9293858622780] , [ 1209528000000 , -3.0769590460943] , [ 1212206400000 , -4.2423933501421] , [ 1214798400000 , -2.6951491617768] , [ 1217476800000 , -2.8981825939957] , [ 1220155200000 , -2.9662727940324] , [ 1222747200000 , 0.21556750497498] , [ 1225425600000 , 2.6784995167088] , [ 1228021200000 , 4.1296711248958] , [ 1230699600000 , 3.7311068218734] , [ 1233378000000 , 4.7695330866954] , [ 1235797200000 , 5.1919133040990] , [ 1238472000000 , 4.1025856045660] , [ 1241064000000 , 2.8498939666225] , [ 1243742400000 , 2.8106017222851] , [ 1246334400000 , 2.8456526669963] , [ 1249012800000 , 0.65563070754298] , [ 1251691200000 , -0.30022343874633] , [ 1254283200000 , -1.1600358228964] , [ 1256961600000 , -0.26674408835052] , [ 1259557200000 , -1.4693389757812] , [ 1262235600000 , -2.7855421590594] , [ 1264914000000 , -1.2668244065703] , [ 1267333200000 , -2.5537804115548] , [ 1270008000000 , -4.9144552474502] , [ 1272600000000 , -6.0484408234831] , [ 1275278400000 , -3.3834349033750] , [ 1277870400000 , -0.46752826932523] , [ 1280548800000 , -1.8030186027963] , [ 1283227200000 , -0.99623230097881] , [ 1285819200000 , -3.3475370235594] , [ 1288497600000 , -3.8187026520342] , [ 1291093200000 , -4.2354146250353] , [ 1293771600000 , -5.6795404292885] , [ 1296450000000 , -6.2928665328172] , [ 1298869200000 , -6.8549277434419] , [ 1301544000000 , -6.9925308360918] , [ 1304136000000 , -8.3216548655839] , [ 1306814400000 , -7.7682867271435] , [ 1309406400000 , -6.9244213301058] , [ 1312084800000 , -5.7407624451404] , [ 1314763200000 , -2.1813149077927] , [ 1317355200000 , 2.9407596325999] , [ 1320033600000 , -1.1130607112134] , [ 1322629200000 , -2.0274822307752] , [ 1325307600000 , -1.8372559072154] , [ 1327986000000 , -4.0732815531148] , [ 1330491600000 , -6.4417038470291]]
      },
      {
        "key": "Series 3",
        "values": [ [ 1025409600000 , 0] , [ 1028088000000 , -6.3382185140371] , [ 1030766400000 , -5.9507873460847] , [ 1033358400000 , -11.569146943813] , [ 1036040400000 , -5.4767332317425] , [ 1038632400000 , 0.50794682203014] , [ 1041310800000 , -5.5310285460542] , [ 1043989200000 , -5.7838296963382] , [ 1046408400000 , -7.3249341615649] , [ 1049086800000 , -6.7078630712489] , [ 1051675200000 , 0.44227126150934] , [ 1054353600000 , 7.2481659343222] , [ 1056945600000 , 9.2512381306992] , [ 1059624000000 , 11.341210982529] , [ 1062302400000 , 14.734820409020] , [ 1064894400000 , 12.387148007542] , [ 1067576400000 , 18.436471461827] , [ 1070168400000 , 19.830742266977] , [ 1072846800000 , 22.643205829887] , [ 1075525200000 , 26.693972514363] , [ 1078030800000 , 29.489903107308] , [ 1080709200000 , 30.756096054034] , [ 1083297600000 , 27.992822746720] , [ 1085976000000 , 29.225852107431] , [ 1088568000000 , 30.156836480689] , [ 1091246400000 , 24.859678459498] , [ 1093924800000 , 24.151326522641] , [ 1096516800000 , 26.974088564049] , [ 1099195200000 , 30.587369307288] , [ 1101790800000 , 35.952410049136] , [ 1104469200000 , 42.723169856608] , [ 1107147600000 , 40.104326572110] , [ 1109566800000 , 42.034940590574] , [ 1112245200000 , 41.201940741519] , [ 1114833600000 , 35.959307673456] , [ 1117512000000 , 40.234785495828] , [ 1120104000000 , 43.347252675906] , [ 1122782400000 , 49.122142270314] , [ 1125460800000 , 46.336213226596] , [ 1128052800000 , 45.738022352292] , [ 1130734800000 , 40.782535587694] , [ 1133326800000 , 46.298919327736] , [ 1136005200000 , 46.525174496692] , [ 1138683600000 , 49.369518277658] , [ 1141102800000 , 51.359233230659] , [ 1143781200000 , 54.290790853085] , [ 1146369600000 , 56.370809889665] , [ 1149048000000 , 52.347251720842] , [ 1151640000000 , 52.651049262704] , [ 1154318400000 , 49.006082346714] , [ 1156996800000 , 53.833722685976] , [ 1159588800000 , 57.368751084016] , [ 1162270800000 , 62.620657436870] , [ 1164862800000 , 67.843814831233] , [ 1167541200000 , 70.696236558827] , [ 1170219600000 , 75.281054033390] , [ 1172638800000 , 75.494257592448] , [ 1175313600000 , 80.620943351778] , [ 1177905600000 , 87.289875534061] , [ 1180584000000 , 93.299043821956] , [ 1183176000000 , 91.015859689151] , [ 1185854400000 , 88.392797582470] , [ 1188532800000 , 94.699212813219] , [ 1191124800000 , 103.50183124741] , [ 1193803200000 , 111.30811970524] , [ 1196398800000 , 101.36138850420] , [ 1199077200000 , 98.665003256909] , [ 1201755600000 , 87.999132307989] , [ 1204261200000 , 85.315653328802] , [ 1206936000000 , 82.146119346213] , [ 1209528000000 , 90.093146599737] , [ 1212206400000 , 99.385987481068] , [ 1214798400000 , 84.763092203314] , [ 1217476800000 , 82.910191547323] , [ 1220155200000 , 90.191781675161] , [ 1222747200000 , 66.188819887335] , [ 1225425600000 , 47.259186154933] , [ 1228021200000 , 40.548648265024] , [ 1230699600000 , 42.458784966634] , [ 1233378000000 , 41.462207260082] , [ 1235797200000 , 35.224936113579] , [ 1238472000000 , 40.810117767284] , [ 1241064000000 , 55.041351655012] , [ 1243742400000 , 59.168485702020] , [ 1246334400000 , 60.474654847301] , [ 1249012800000 , 67.306616497709] , [ 1251691200000 , 70.539019993440] , [ 1254283200000 , 77.571962668603] , [ 1256961600000 , 72.108784451998] , [ 1259557200000 , 80.269048905849] , [ 1262235600000 , 84.754250235173] , [ 1264914000000 , 83.053938255703] , [ 1267333200000 , 88.067497980334] , [ 1270008000000 , 97.556993569060] , [ 1272600000000 , 96.744762710807] , [ 1275278400000 , 87.146301147104] , [ 1277870400000 , 76.113331725206] , [ 1280548800000 , 84.745960774176] , [ 1283227200000 , 80.883421033110] , [ 1285819200000 , 98.377963136001] , [ 1288497600000 , 104.16094587057] , [ 1291093200000 , 101.92699168281] , [ 1293771600000 , 109.16314556604] , [ 1296450000000 , 115.31506669000] , [ 1298869200000 , 126.55944572261] , [ 1301544000000 , 118.47392959295] , [ 1304136000000 , 121.44619467743] , [ 1306814400000 , 120.38970188330] , [ 1309406400000 , 114.99946573061] , [ 1312084800000 , 110.95959856356] , [ 1314763200000 , 86.186386929240] , [ 1317355200000 , 62.100425398325] , [ 1320033600000 , 78.680507428540] , [ 1322629200000 , 73.876351797642] , [ 1325307600000 , 70.866962301942] , [ 1327986000000 , 80.863709250982] , [ 1330491600000 , 86.946444823715]]
      },
      {
        "key": "Series 4",
        "values": [ [ 1025409600000 , -7.0674410638835] , [ 1028088000000 , -14.663359292964] , [ 1030766400000 , -14.104393060540] , [ 1033358400000 , -23.114477037218] , [ 1036040400000 , -16.774256687841] , [ 1038632400000 , -11.902028464000] , [ 1041310800000 , -16.883038668422] , [ 1043989200000 , -19.104223676831] , [ 1046408400000 , -20.420523282736] , [ 1049086800000 , -19.660555051587] , [ 1051675200000 , -13.106911231646] , [ 1054353600000 , -8.2448460302143] , [ 1056945600000 , -7.0313058730976] , [ 1059624000000 , -5.1485118700389] , [ 1062302400000 , -3.0011028761469] , [ 1064894400000 , -4.1367265281467] , [ 1067576400000 , 1.5425209565025] , [ 1070168400000 , 2.7673533607299] , [ 1072846800000 , 7.7077114755360] , [ 1075525200000 , 9.7565015112434] , [ 1078030800000 , 11.396888609473] , [ 1080709200000 , 10.013964745578] , [ 1083297600000 , 8.0558890950562] , [ 1085976000000 , 9.6081966657458] , [ 1088568000000 , 11.918590426432] , [ 1091246400000 , 7.9945345523982] , [ 1093924800000 , 8.3201276776796] , [ 1096516800000 , 9.8283954846342] , [ 1099195200000 , 11.527125859650] , [ 1101790800000 , 16.413657596527] , [ 1104469200000 , 20.393798297928] , [ 1107147600000 , 17.456308413907] , [ 1109566800000 , 20.087778400999] , [ 1112245200000 , 17.988336990817] , [ 1114833600000 , 15.378490151331] , [ 1117512000000 , 19.474322935730] , [ 1120104000000 , 20.013851070354] , [ 1122782400000 , 24.749943726975] , [ 1125460800000 , 23.558710274826] , [ 1128052800000 , 24.558915040889] , [ 1130734800000 , 22.355860488034] , [ 1133326800000 , 27.138026265756] , [ 1136005200000 , 27.202220808591] , [ 1138683600000 , 31.219437344964] , [ 1141102800000 , 31.392355525125] , [ 1143781200000 , 33.373099232542] , [ 1146369600000 , 35.095277582309] , [ 1149048000000 , 30.923356507615] , [ 1151640000000 , 31.083717332561] , [ 1154318400000 , 31.290690671561] , [ 1156996800000 , 34.247769216679] , [ 1159588800000 , 37.411073177620] , [ 1162270800000 , 42.079177096411] , [ 1164862800000 , 44.978191659648] , [ 1167541200000 , 46.713271025310] , [ 1170219600000 , 49.203892437699] , [ 1172638800000 , 46.684723471826] , [ 1175313600000 , 48.385458973500] , [ 1177905600000 , 54.660197840305] , [ 1180584000000 , 60.311838415602] , [ 1183176000000 , 57.583282204682] , [ 1185854400000 , 52.425398898751] , [ 1188532800000 , 54.663538086985] , [ 1191124800000 , 60.181844325224] , [ 1193803200000 , 62.877219773621] , [ 1196398800000 , 55.760611512951] , [ 1199077200000 , 54.735280367784] , [ 1201755600000 , 45.495912959474] , [ 1204261200000 , 40.934919015876] , [ 1206936000000 , 40.303777633187] , [ 1209528000000 , 47.403740368773] , [ 1212206400000 , 49.951960898839] , [ 1214798400000 , 37.534590035098] , [ 1217476800000 , 36.405758293321] , [ 1220155200000 , 38.545373001858] , [ 1222747200000 , 26.106358664455] , [ 1225425600000 , 4.2658006768744] , [ 1228021200000 , -3.5517839867557] , [ 1230699600000 , -2.0878920761513] , [ 1233378000000 , -10.408879093829] , [ 1235797200000 , -19.924242196038] , [ 1238472000000 , -12.906491912782] , [ 1241064000000 , -3.9774866468346] , [ 1243742400000 , 1.0319171601402] , [ 1246334400000 , 1.3109350357718] , [ 1249012800000 , 9.1668309061935] , [ 1251691200000 , 13.121178985954] , [ 1254283200000 , 17.578680237511] , [ 1256961600000 , 14.971294355085] , [ 1259557200000 , 21.551327027338] , [ 1262235600000 , 24.592328423819] , [ 1264914000000 , 20.158087829555] , [ 1267333200000 , 24.135661929185] , [ 1270008000000 , 31.815205405903] , [ 1272600000000 , 34.389524768466] , [ 1275278400000 , 23.785555857522] , [ 1277870400000 , 17.082756649072] , [ 1280548800000 , 25.248007727100] , [ 1283227200000 , 19.415179069165] , [ 1285819200000 , 30.413636349327] , [ 1288497600000 , 35.357952964550] , [ 1291093200000 , 35.886413535859] , [ 1293771600000 , 45.003601951959] , [ 1296450000000 , 48.274893564020] , [ 1298869200000 , 53.562864914648] , [ 1301544000000 , 54.108274337412] , [ 1304136000000 , 58.618190111927] , [ 1306814400000 , 56.806793965598] , [ 1309406400000 , 54.135477252994] , [ 1312084800000 , 50.735258942442] , [ 1314763200000 , 42.208170945813] , [ 1317355200000 , 31.617916826724] , [ 1320033600000 , 46.492005006737] , [ 1322629200000 , 46.203116922145] , [ 1325307600000 , 47.541427643137] , [ 1327986000000 , 54.518998440993] , [ 1330491600000 , 61.099720234693]]
      }
    ]
}
function oochart_comulativeline_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
      var chart = nv.models.cumulativeLineChart()
        .x(function(d) { return d[0] })
        //adjusting, 100% is 1.00, not 100 as it is in the data
        .y(function(d) { return d[1] / 100 })
        .color(d3.scale.category10().range())
        .useInteractiveGuideline(true)
        ;

      chart.xAxis
        .tickFormat(function(d) {
          return d3.time.format('%x')(new Date(d))
        });

      chart.yAxis.tickFormat(d3.format(',.1%'));

      svg_d3.datum(data)
        .transition().duration(duration)
        .call(chart)
        ;

      nv.utils.windowResize(chart.update);

      return chart;
    },function(){
        if(simple){
            svg_d3.selectAll('text').remove();
            svg_d3.selectAll('.nv-axis').remove()
            svg_d3.selectAll('.nv-legendWrap').remove()
            svg_d3.selectAll('.nv-controlsWrap').remove()

        };
    });

}

function oochart_line_plus_bar_example_data(){
    return [
      {
        "key" : "Quantity",
        "bar": true,
        "values" : [ [ 1136005200000 , 1271000.0] , [ 1138683600000 , 1271000.0] , [ 1141102800000 , 1271000.0] , [ 1143781200000 , 0] , [ 1146369600000 , 0] , [ 1149048000000 , 0] , [ 1151640000000 , 0] , [ 1154318400000 , 0] , [ 1156996800000 , 0] , [ 1159588800000 , 3899486.0] , [ 1162270800000 , 3899486.0] , [ 1164862800000 , 3899486.0] , [ 1167541200000 , 3564700.0] , [ 1170219600000 , 3564700.0] , [ 1172638800000 , 3564700.0] , [ 1175313600000 , 2648493.0] , [ 1177905600000 , 2648493.0] , [ 1180584000000 , 2648493.0] , [ 1183176000000 , 2522993.0] , [ 1185854400000 , 2522993.0] , [ 1188532800000 , 2522993.0] , [ 1191124800000 , 2906501.0] , [ 1193803200000 , 2906501.0] , [ 1196398800000 , 2906501.0] , [ 1199077200000 , 2206761.0] , [ 1201755600000 , 2206761.0] , [ 1204261200000 , 2206761.0] , [ 1206936000000 , 2287726.0] , [ 1209528000000 , 2287726.0] , [ 1212206400000 , 2287726.0] , [ 1214798400000 , 2732646.0] , [ 1217476800000 , 2732646.0] , [ 1220155200000 , 2732646.0] , [ 1222747200000 , 2599196.0] , [ 1225425600000 , 2599196.0] , [ 1228021200000 , 2599196.0] , [ 1230699600000 , 1924387.0] , [ 1233378000000 , 1924387.0] , [ 1235797200000 , 1924387.0] , [ 1238472000000 , 1756311.0] , [ 1241064000000 , 1756311.0] , [ 1243742400000 , 1756311.0] , [ 1246334400000 , 1743470.0] , [ 1249012800000 , 1743470.0] , [ 1251691200000 , 1743470.0] , [ 1254283200000 , 1519010.0] , [ 1256961600000 , 1519010.0] , [ 1259557200000 , 1519010.0] , [ 1262235600000 , 1591444.0] , [ 1264914000000 , 1591444.0] , [ 1267333200000 , 1591444.0] , [ 1270008000000 , 1543784.0] , [ 1272600000000 , 1543784.0] , [ 1275278400000 , 1543784.0] , [ 1277870400000 , 1309915.0] , [ 1280548800000 , 1309915.0] , [ 1283227200000 , 1309915.0] , [ 1285819200000 , 1331875.0] , [ 1288497600000 , 1331875.0] , [ 1291093200000 , 1331875.0] , [ 1293771600000 , 1331875.0] , [ 1296450000000 , 1154695.0] , [ 1298869200000 , 1154695.0] , [ 1301544000000 , 1194025.0] , [ 1304136000000 , 1194025.0] , [ 1306814400000 , 1194025.0] , [ 1309406400000 , 1194025.0] , [ 1312084800000 , 1194025.0] , [ 1314763200000 , 1244525.0] , [ 1317355200000 , 475000.0] , [ 1320033600000 , 475000.0] , [ 1322629200000 , 475000.0] , [ 1325307600000 , 690033.0] , [ 1327986000000 , 690033.0] , [ 1330491600000 , 690033.0] , [ 1333166400000 , 514733.0] , [ 1335758400000 , 514733.0]]
      },
      {
        "key" : "Price",
        "values" : [ [ 1136005200000 , 71.89] , [ 1138683600000 , 75.51] , [ 1141102800000 , 68.49] , [ 1143781200000 , 62.72] , [ 1146369600000 , 70.39] , [ 1149048000000 , 59.77] , [ 1151640000000 , 57.27] , [ 1154318400000 , 67.96] , [ 1156996800000 , 67.85] , [ 1159588800000 , 76.98] , [ 1162270800000 , 81.08] , [ 1164862800000 , 91.66] , [ 1167541200000 , 84.84] , [ 1170219600000 , 85.73] , [ 1172638800000 , 84.61] , [ 1175313600000 , 92.91] , [ 1177905600000 , 99.8] , [ 1180584000000 , 121.191] , [ 1183176000000 , 122.04] , [ 1185854400000 , 131.76] , [ 1188532800000 , 138.48] , [ 1191124800000 , 153.47] , [ 1193803200000 , 189.95] , [ 1196398800000 , 182.22] , [ 1199077200000 , 198.08] , [ 1201755600000 , 135.36] , [ 1204261200000 , 125.02] , [ 1206936000000 , 143.5] , [ 1209528000000 , 173.95] , [ 1212206400000 , 188.75] , [ 1214798400000 , 167.44] , [ 1217476800000 , 158.95] , [ 1220155200000 , 169.53] , [ 1222747200000 , 113.66] , [ 1225425600000 , 107.59] , [ 1228021200000 , 92.67] , [ 1230699600000 , 85.35] , [ 1233378000000 , 90.13] , [ 1235797200000 , 89.31] , [ 1238472000000 , 105.12] , [ 1241064000000 , 125.83] , [ 1243742400000 , 135.81] , [ 1246334400000 , 142.43] , [ 1249012800000 , 163.39] , [ 1251691200000 , 168.21] , [ 1254283200000 , 185.35] , [ 1256961600000 , 188.5] , [ 1259557200000 , 199.91] , [ 1262235600000 , 210.732] , [ 1264914000000 , 192.063] , [ 1267333200000 , 204.62] , [ 1270008000000 , 235.0] , [ 1272600000000 , 261.09] , [ 1275278400000 , 256.88] , [ 1277870400000 , 251.53] , [ 1280548800000 , 257.25] , [ 1283227200000 , 243.1] , [ 1285819200000 , 283.75] , [ 1288497600000 , 300.98] , [ 1291093200000 , 311.15] , [ 1293771600000 , 322.56] , [ 1296450000000 , 339.32] , [ 1298869200000 , 353.21] , [ 1301544000000 , 348.5075] , [ 1304136000000 , 350.13] , [ 1306814400000 , 347.83] , [ 1309406400000 , 335.67] , [ 1312084800000 , 390.48] , [ 1314763200000 , 384.83] , [ 1317355200000 , 381.32] , [ 1320033600000 , 404.78] , [ 1322629200000 , 382.2] , [ 1325307600000 , 405.0] , [ 1327986000000 , 456.48] , [ 1330491600000 , 542.44] , [ 1333166400000 , 599.55] , [ 1335758400000 , 583.98]]
      }
    ]
}
function oochart_lineplusbar_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
        var chart = nv.models.linePlusBarChart()
          .margin({top: 30, right: 60, bottom: 50, left: 70})
          .x(function(d,i) { return i })
          .y(function(d) { return d[1] })
          .color(d3.scale.category10().range())
          ;
        if(simple){
            chart.showLegend(false);
        };
        chart.xAxis
          .showMaxMin(false)
          .tickFormat(function(d) {
            var dx = data[0].values[d] && data[0].values[d][0] || 0;
            return d3.time.format('%x')(new Date(dx))
          });

        chart.y1Axis
          .tickFormat(d3.format(',f'));

        chart.y2Axis
          .tickFormat(function(d) { return '$' + d3.format(',f')(d) });

        chart.bars.forceY([0]);

        svg_d3.datum(data)
          .transition().duration(duration)
          .call(chart)
          ;

        nv.utils.windowResize(chart.update);

        return chart;
    },function(){
        svg_d3.selectAll('.nv-legendWrap').remove();
        svg_d3.selectAll('.nv-axis').remove();

    });

}

function oochart_hgsbar_example_data(){
    return [
      {
        "key": "Series1",
        "color": "#d62728",
        "values": [
          {
            "label" : "Group A" ,
            "value" : -1.8746444827653
          } ,
          {
            "label" : "Group B" ,
            "value" : -8.0961543492239
          } ,
          {
            "label" : "Group C" ,
            "value" : -0.57072943117674
          } ,
          {
            "label" : "Group D" ,
            "value" : -2.4174010336624
          } ,
          {
            "label" : "Group E" ,
            "value" : -0.72009071426284
          } ,
          {
            "label" : "Group F" ,
            "value" : -0.77154485523777
          } ,
          {
            "label" : "Group G" ,
            "value" : -0.90152097798131
          } ,
          {
            "label" : "Group H" ,
            "value" : -0.91445417330854
          } ,
          {
            "label" : "Group I" ,
            "value" : -0.055746319141851
          }
        ]
      },
      {
        "key": "Series2",
        "color": "#1f77b4",
        "values": [
          {
            "label" : "Group A" ,
            "value" : 25.307646510375
          } ,
          {
            "label" : "Group B" ,
            "value" : 16.756779544553
          } ,
          {
            "label" : "Group C" ,
            "value" : 18.451534877007
          } ,
          {
            "label" : "Group D" ,
            "value" : 8.6142352811805
          } ,
          {
            "label" : "Group E" ,
            "value" : 7.8082472075876
          } ,
          {
            "label" : "Group F" ,
            "value" : 5.259101026956
          } ,
          {
            "label" : "Group G" ,
            "value" : 0.30947953487127
          } ,
          {
            "label" : "Group H" ,
            "value" : 0
          } ,
          {
            "label" : "Group I" ,
            "value" : 0
          }
        ]
      }
    ]
}
function oochart_hgsbar_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
      var chart = nv.models.multiBarHorizontalChart()
          .x(function(d) { return d.label })
          .y(function(d) { return d.value })
          .margin({top: 30, right: 20, bottom: 50, left: 175})
          .showValues(true)
          .showControls(false);
      if(simple){
            chart.showLegend(false).showControls(false).showXAxis(false).showYAxis(false);
        };
      chart.yAxis
          .tickFormat(d3.format(',.2f'));

      svg_d3.datum(data)
        .transition().duration(duration)
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
}

function ootable_descrete_bar_example_data(){
    return [
      {
        key: "Cumulative Return",
        values: [
          {
            "label" : "A" ,
            "value" : -29.765957771107
          } ,
          {
            "label" : "B" ,
            "value" : 0
          } ,
          {
            "label" : "C" ,
            "value" : 32.807804682612
          } ,
          {
            "label" : "D" ,
            "value" : 196.45946739256
          } ,
          {
            "label" : "E" ,
            "value" : 0.19434030906893
          } ,
          {
            "label" : "F" ,
            "value" : -98.079782601442
          } ,
          {
            "label" : "G" ,
            "value" : -13.925743130903
          } ,
          {
            "label" : "H" ,
            "value" : -5.1387322875705
          }
        ]
      }
    ]
}
function oochart_discretebar_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
      var svg_d3 = oochart_create_svg(svg_id,svg);
      nv.addGraph(function() {
          var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            .showValues(true)
          if(simple){
                chart.showLegend(false).showControls(false).showXAxis(false).showYAxis(false);
            };
          svg_d3.datum(data)
            .transition().duration(duration)
            .call(chart)
            ;

          nv.utils.windowResize(chart.update);

          return chart;
        });
}

function oochart_stackedarea_example_data(){
    return [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] , [ 1033358400000 , 22.093608385173] , [ 1036040400000 , 25.108079299458] , [ 1038632400000 , 26.982389242348] , [ 1041310800000 , 19.828984957662] , [ 1043989200000 , 19.914055036294] , [ 1046408400000 , 19.436150539916] , [ 1049086800000 , 21.558650338602] , [ 1051675200000 , 24.395594061773] , [ 1054353600000 , 24.747089309384] , [ 1056945600000 , 23.491755498807] , [ 1059624000000 , 23.376634878164] , [ 1062302400000 , 24.581223154533] , [ 1064894400000 , 24.922476843538] , [ 1067576400000 , 27.357712939042] , [ 1070168400000 , 26.503020572593] , [ 1072846800000 , 26.658901244878] , [ 1075525200000 , 27.065704156445] , [ 1078030800000 , 28.735320452588] , [ 1080709200000 , 31.572277846319] , [ 1083297600000 , 30.932161503638] , [ 1085976000000 , 31.627029785554] , [ 1088568000000 , 28.728743674232] , [ 1091246400000 , 26.858365172675] , [ 1093924800000 , 27.279922830032] , [ 1096516800000 , 34.408301211324] , [ 1099195200000 , 34.794362930439] , [ 1101790800000 , 35.609978198951] , [ 1104469200000 , 33.574394968037] , [ 1107147600000 , 31.979405070598] , [ 1109566800000 , 31.19009040297] , [ 1112245200000 , 31.083933968994] , [ 1114833600000 , 29.668971113185] , [ 1117512000000 , 31.490638014379] , [ 1120104000000 , 31.818617451128] , [ 1122782400000 , 32.960314008183] , [ 1125460800000 , 31.313383196209] , [ 1128052800000 , 33.125486081852] , [ 1130734800000 , 32.791805509149] , [ 1133326800000 , 33.506038030366] , [ 1136005200000 , 26.96501697216] , [ 1138683600000 , 27.38478809681] , [ 1141102800000 , 27.371377218209] , [ 1143781200000 , 26.309915460827] , [ 1146369600000 , 26.425199957518] , [ 1149048000000 , 26.823411519396] , [ 1151640000000 , 23.850443591587] , [ 1154318400000 , 23.158355444054] , [ 1156996800000 , 22.998689393695] , [ 1159588800000 , 27.9771285113] , [ 1162270800000 , 29.073672469719] , [ 1164862800000 , 28.587640408904] , [ 1167541200000 , 22.788453687637] , [ 1170219600000 , 22.429199073597] , [ 1172638800000 , 22.324103271052] , [ 1175313600000 , 17.558388444187] , [ 1177905600000 , 16.769518096208] , [ 1180584000000 , 16.214738201301] , [ 1183176000000 , 18.729632971229] , [ 1185854400000 , 18.814523318847] , [ 1188532800000 , 19.789986451358] , [ 1191124800000 , 17.070049054933] , [ 1193803200000 , 16.121349575716] , [ 1196398800000 , 15.141659430091] , [ 1199077200000 , 17.175388025297] , [ 1201755600000 , 17.286592443522] , [ 1204261200000 , 16.323141626568] , [ 1206936000000 , 19.231263773952] , [ 1209528000000 , 18.446256391095] , [ 1212206400000 , 17.822632399764] , [ 1214798400000 , 15.53936647598] , [ 1217476800000 , 15.255131790217] , [ 1220155200000 , 15.660963922592] , [ 1222747200000 , 13.254482273698] , [ 1225425600000 , 11.920796202299] , [ 1228021200000 , 12.122809090924] , [ 1230699600000 , 15.691026271393] , [ 1233378000000 , 14.720881635107] , [ 1235797200000 , 15.387939360044] , [ 1238472000000 , 13.765436672228] , [ 1241064000000 , 14.631445864799] , [ 1243742400000 , 14.292446536221] , [ 1246334400000 , 16.170071367017] , [ 1249012800000 , 15.948135554337] , [ 1251691200000 , 16.612872685134] , [ 1254283200000 , 18.778338719091] , [ 1256961600000 , 16.756026065421] , [ 1259557200000 , 19.385804443146] , [ 1262235600000 , 22.950590240168] , [ 1264914000000 , 23.61159018141] , [ 1267333200000 , 25.708586989581] , [ 1270008000000 , 26.883915999885] , [ 1272600000000 , 25.893486687065] , [ 1275278400000 , 24.678914263176] , [ 1277870400000 , 25.937275793024] , [ 1280548800000 , 29.461381693838] , [ 1283227200000 , 27.357322961861] , [ 1285819200000 , 29.057235285673] , [ 1288497600000 , 28.549434189386] , [ 1291093200000 , 28.506352379724] , [ 1293771600000 , 29.449241421598] , [ 1296450000000 , 25.796838168807] , [ 1298869200000 , 28.740145449188] , [ 1301544000000 , 22.091744141872] , [ 1304136000000 , 25.07966254541] , [ 1306814400000 , 23.674906973064] , [ 1309406400000 , 23.418002742929] , [ 1312084800000 , 23.24364413887] , [ 1314763200000 , 31.591854066817] , [ 1317355200000 , 31.497112374114] , [ 1320033600000 , 26.67238082043] , [ 1322629200000 , 27.297080015495] , [ 1325307600000 , 20.174315530051] , [ 1327986000000 , 19.631084213898] , [ 1330491600000 , 20.366462219461] , [ 1333166400000 , 19.284784434185] , [ 1335758400000 , 19.157810257624]]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] , [ 1033358400000 , 5.8996782364764] , [ 1036040400000 , 6.0591869346923] , [ 1038632400000 , 5.9667815800451] , [ 1041310800000 , 8.65528925664] , [ 1043989200000 , 8.7690763386254] , [ 1046408400000 , 8.6386160387453] , [ 1049086800000 , 5.9895557449743] , [ 1051675200000 , 6.3840324338159] , [ 1054353600000 , 6.5196511461441] , [ 1056945600000 , 7.0738618553114] , [ 1059624000000 , 6.5745957367133] , [ 1062302400000 , 6.4658359184444] , [ 1064894400000 , 2.7622758754954] , [ 1067576400000 , 2.9794782986241] , [ 1070168400000 , 2.8735432712019] , [ 1072846800000 , 1.6344817513645] , [ 1075525200000 , 1.5869248754883] , [ 1078030800000 , 1.7172279157246] , [ 1080709200000 , 1.9649927409867] , [ 1083297600000 , 2.0261695079196] , [ 1085976000000 , 2.0541261923929] , [ 1088568000000 , 3.9466318927569] , [ 1091246400000 , 3.7826770946089] , [ 1093924800000 , 3.9543021004028] , [ 1096516800000 , 3.8309891064711] , [ 1099195200000 , 3.6340958946166] , [ 1101790800000 , 3.5289755762525] , [ 1104469200000 , 5.702378559857] , [ 1107147600000 , 5.6539569019223] , [ 1109566800000 , 5.5449506370392] , [ 1112245200000 , 4.7579993280677] , [ 1114833600000 , 4.4816139372906] , [ 1117512000000 , 4.5965558568606] , [ 1120104000000 , 4.3747066116976] , [ 1122782400000 , 4.4588822917087] , [ 1125460800000 , 4.4460351848286] , [ 1128052800000 , 3.7989113035136] , [ 1130734800000 , 3.7743883140088] , [ 1133326800000 , 3.7727852823828] , [ 1136005200000 , 7.2968111448895] , [ 1138683600000 , 7.2800122043237] , [ 1141102800000 , 7.1187787503354] , [ 1143781200000 , 8.351887016482] , [ 1146369600000 , 8.4156698763993] , [ 1149048000000 , 8.1673298604231] , [ 1151640000000 , 5.5132447126042] , [ 1154318400000 , 6.1152537710599] , [ 1156996800000 , 6.076765091942] , [ 1159588800000 , 4.6304473798646] , [ 1162270800000 , 4.6301068469402] , [ 1164862800000 , 4.3466656309389] , [ 1167541200000 , 6.830104897003] , [ 1170219600000 , 7.241633040029] , [ 1172638800000 , 7.1432372054153] , [ 1175313600000 , 10.608942063374] , [ 1177905600000 , 10.914964549494] , [ 1180584000000 , 10.933223880565] , [ 1183176000000 , 8.3457524851265] , [ 1185854400000 , 8.1078413081882] , [ 1188532800000 , 8.2697185922474] , [ 1191124800000 , 8.4742436475968] , [ 1193803200000 , 8.4994601179319] , [ 1196398800000 , 8.7387319683243] , [ 1199077200000 , 6.8829183612895] , [ 1201755600000 , 6.984133637885] , [ 1204261200000 , 7.0860136043287] , [ 1206936000000 , 4.3961787956053] , [ 1209528000000 , 3.8699674365231] , [ 1212206400000 , 3.6928925238305] , [ 1214798400000 , 6.7571718894253] , [ 1217476800000 , 6.4367313362344] , [ 1220155200000 , 6.4048441521454] , [ 1222747200000 , 5.4643833239669] , [ 1225425600000 , 5.3150786833374] , [ 1228021200000 , 5.3011272612576] , [ 1230699600000 , 4.1203601430809] , [ 1233378000000 , 4.0881783200525] , [ 1235797200000 , 4.1928665957189] , [ 1238472000000 , 7.0249415663205] , [ 1241064000000 , 7.006530880769] , [ 1243742400000 , 6.994835633224] , [ 1246334400000 , 6.1220222336254] , [ 1249012800000 , 6.1177436137653] , [ 1251691200000 , 6.1413396231981] , [ 1254283200000 , 4.8046006145874] , [ 1256961600000 , 4.6647600660544] , [ 1259557200000 , 4.544865006255] , [ 1262235600000 , 6.0488249316539] , [ 1264914000000 , 6.3188669540206] , [ 1267333200000 , 6.5873958262306] , [ 1270008000000 , 6.2281189839578] , [ 1272600000000 , 5.8948915746059] , [ 1275278400000 , 5.5967320482214] , [ 1277870400000 , 0.99784432084837] , [ 1280548800000 , 1.0950794175359] , [ 1283227200000 , 0.94479734407491] , [ 1285819200000 , 1.222093988688] , [ 1288497600000 , 1.335093106856] , [ 1291093200000 , 1.3302565104985] , [ 1293771600000 , 1.340824670897] , [ 1296450000000 , 0] , [ 1298869200000 , 0] , [ 1301544000000 , 0] , [ 1304136000000 , 0] , [ 1306814400000 , 0] , [ 1309406400000 , 0] , [ 1312084800000 , 0] , [ 1314763200000 , 0] , [ 1317355200000 , 4.4583692315] , [ 1320033600000 , 3.6493043348059] , [ 1322629200000 , 3.8610064091761] , [ 1325307600000 , 5.5144800685202] , [ 1327986000000 , 5.1750695220791] , [ 1330491600000 , 5.6710066952691] , [ 1333166400000 , 5.5611890039181] , [ 1335758400000 , 5.5979368839939]]
    },

    {
      "key" : "South America" ,
      "values" : [ [ 1025409600000 , 7.9149900245423] , [ 1028088000000 , 7.0899888751059] , [ 1030766400000 , 7.5996132380614] , [ 1033358400000 , 8.2741174301034] , [ 1036040400000 , 9.3564460833513] , [ 1038632400000 , 9.7066786059904] , [ 1041310800000 , 10.213363052343] , [ 1043989200000 , 10.285809585273] , [ 1046408400000 , 10.222053149228] , [ 1049086800000 , 8.6188592137975] , [ 1051675200000 , 9.3335447543566] , [ 1054353600000 , 8.9312402186628] , [ 1056945600000 , 8.1895089343658] , [ 1059624000000 , 8.260622135079] , [ 1062302400000 , 7.7700786851364] , [ 1064894400000 , 7.9907428771318] , [ 1067576400000 , 8.7769091865606] , [ 1070168400000 , 8.4855077060661] , [ 1072846800000 , 9.6277203033655] , [ 1075525200000 , 9.9685913452624] , [ 1078030800000 , 10.615085181759] , [ 1080709200000 , 9.2902488079646] , [ 1083297600000 , 8.8610439830061] , [ 1085976000000 , 9.1075344931229] , [ 1088568000000 , 9.9156737639203] , [ 1091246400000 , 9.7826003238782] , [ 1093924800000 , 10.55403610555] , [ 1096516800000 , 10.926900264097] , [ 1099195200000 , 10.903144818736] , [ 1101790800000 , 10.862890389067] , [ 1104469200000 , 10.64604998964] , [ 1107147600000 , 10.042790814087] , [ 1109566800000 , 9.7173391591038] , [ 1112245200000 , 9.6122415755443] , [ 1114833600000 , 9.4337921146562] , [ 1117512000000 , 9.814827171183] , [ 1120104000000 , 12.059260396788] , [ 1122782400000 , 12.139649903873] , [ 1125460800000 , 12.281290663822] , [ 1128052800000 , 8.8037085409056] , [ 1130734800000 , 8.6300618239176] , [ 1133326800000 , 9.1225708491432] , [ 1136005200000 , 12.988124170836] , [ 1138683600000 , 13.356778764353] , [ 1141102800000 , 13.611196863271] , [ 1143781200000 , 6.8959030061189] , [ 1146369600000 , 6.9939633271353] , [ 1149048000000 , 6.7241510257676] , [ 1151640000000 , 5.5611293669517] , [ 1154318400000 , 5.6086488714041] , [ 1156996800000 , 5.4962849907033] , [ 1159588800000 , 6.9193153169278] , [ 1162270800000 , 7.0016334389778] , [ 1164862800000 , 6.7865422443273] , [ 1167541200000 , 9.0006454225383] , [ 1170219600000 , 9.2233916171431] , [ 1172638800000 , 8.8929316009479] , [ 1175313600000 , 10.345937520404] , [ 1177905600000 , 10.075914677026] , [ 1180584000000 , 10.089006188111] , [ 1183176000000 , 10.598330295008] , [ 1185854400000 , 9.9689546533009] , [ 1188532800000 , 9.7740580198146] , [ 1191124800000 , 10.558483060626] , [ 1193803200000 , 9.9314651823603] , [ 1196398800000 , 9.3997715873769] , [ 1199077200000 , 8.4086493387262] , [ 1201755600000 , 8.9698309085926] , [ 1204261200000 , 8.2778357995396] , [ 1206936000000 , 8.8585045600123] , [ 1209528000000 , 8.7013756413322] , [ 1212206400000 , 7.7933605469443] , [ 1214798400000 , 7.0236183483064] , [ 1217476800000 , 6.9873088186829] , [ 1220155200000 , 6.8031713070097] , [ 1222747200000 , 6.6869531315723] , [ 1225425600000 , 6.138256993963] , [ 1228021200000 , 5.6434994016354] , [ 1230699600000 , 5.495220262512] , [ 1233378000000 , 4.6885326869846] , [ 1235797200000 , 4.4524349883438] , [ 1238472000000 , 5.6766520778185] , [ 1241064000000 , 5.7675774480752] , [ 1243742400000 , 5.7882863168337] , [ 1246334400000 , 7.2666010034924] , [ 1249012800000 , 7.5191821322261] , [ 1251691200000 , 7.849651451445] , [ 1254283200000 , 10.383992037985] , [ 1256961600000 , 9.0653691861818] , [ 1259557200000 , 9.6705248324159] , [ 1262235600000 , 10.856380561349] , [ 1264914000000 , 11.27452370892] , [ 1267333200000 , 11.754156529088] , [ 1270008000000 , 8.2870811422455] , [ 1272600000000 , 8.0210264360699] , [ 1275278400000 , 7.5375074474865] , [ 1277870400000 , 8.3419527338039] , [ 1280548800000 , 9.4197471818443] , [ 1283227200000 , 8.7321733185797] , [ 1285819200000 , 9.6627062648126] , [ 1288497600000 , 10.187962234548] , [ 1291093200000 , 9.8144201733476] , [ 1293771600000 , 10.275723361712] , [ 1296450000000 , 16.796066079353] , [ 1298869200000 , 17.543254984075] , [ 1301544000000 , 16.673660675083] , [ 1304136000000 , 17.963944353609] , [ 1306814400000 , 16.63774086721] , [ 1309406400000 , 15.84857094609] , [ 1312084800000 , 14.767303362181] , [ 1314763200000 , 24.778452182433] , [ 1317355200000 , 18.370353229999] , [ 1320033600000 , 15.253137429099] , [ 1322629200000 , 14.989600840649] , [ 1325307600000 , 16.052539160125] , [ 1327986000000 , 16.424390322793] , [ 1330491600000 , 17.884020741104] , [ 1333166400000 , 18.372698836036] , [ 1335758400000 , 18.315881576096]]
    },

    {
      "key" : "Asia" ,
      "values" : [ [ 1025409600000 , 13.153938631352] , [ 1028088000000 , 12.456410521864] , [ 1030766400000 , 12.537048663919] , [ 1033358400000 , 13.947386398309] , [ 1036040400000 , 14.421680682568] , [ 1038632400000 , 14.143238262286] , [ 1041310800000 , 12.229635347478] , [ 1043989200000 , 12.508479916948] , [ 1046408400000 , 12.155368409526] , [ 1049086800000 , 13.335455563994] , [ 1051675200000 , 12.888210138167] , [ 1054353600000 , 12.842092790511] , [ 1056945600000 , 12.513816474199] , [ 1059624000000 , 12.21453674494] , [ 1062302400000 , 11.750848343935] , [ 1064894400000 , 10.526579636787] , [ 1067576400000 , 10.873596086087] , [ 1070168400000 , 11.019967131519] , [ 1072846800000 , 11.235789380602] , [ 1075525200000 , 11.859910850657] , [ 1078030800000 , 12.531031616536] , [ 1080709200000 , 11.360451067019] , [ 1083297600000 , 11.456244780202] , [ 1085976000000 , 11.436991407309] , [ 1088568000000 , 11.638595744327] , [ 1091246400000 , 11.190418301469] , [ 1093924800000 , 11.835608007589] , [ 1096516800000 , 11.540980244475] , [ 1099195200000 , 10.958762325687] , [ 1101790800000 , 10.885791159509] , [ 1104469200000 , 13.605810720109] , [ 1107147600000 , 13.128978067437] , [ 1109566800000 , 13.119012086882] , [ 1112245200000 , 13.003706129783] , [ 1114833600000 , 13.326996807689] , [ 1117512000000 , 13.547947991743] , [ 1120104000000 , 12.807959646616] , [ 1122782400000 , 12.931763821068] , [ 1125460800000 , 12.795359993008] , [ 1128052800000 , 9.6998935538319] , [ 1130734800000 , 9.3473740089131] , [ 1133326800000 , 9.36902067716] , [ 1136005200000 , 14.258619539875] , [ 1138683600000 , 14.21241095603] , [ 1141102800000 , 13.973193618249] , [ 1143781200000 , 15.218233920664] , [ 1146369600000 , 14.382109727451] , [ 1149048000000 , 13.894310878491] , [ 1151640000000 , 15.593086090031] , [ 1154318400000 , 16.244839695189] , [ 1156996800000 , 16.017088850647] , [ 1159588800000 , 14.183951830057] , [ 1162270800000 , 14.148523245696] , [ 1164862800000 , 13.424326059971] , [ 1167541200000 , 12.974450435754] , [ 1170219600000 , 13.232470418021] , [ 1172638800000 , 13.318762655574] , [ 1175313600000 , 15.961407746104] , [ 1177905600000 , 16.287714639805] , [ 1180584000000 , 16.24659058389] , [ 1183176000000 , 17.564505594808] , [ 1185854400000 , 17.872725373164] , [ 1188532800000 , 18.018998508756] , [ 1191124800000 , 15.584518016602] , [ 1193803200000 , 15.480850647182] , [ 1196398800000 , 15.699120036985] , [ 1199077200000 , 19.184281817226] , [ 1201755600000 , 19.691226605205] , [ 1204261200000 , 18.982314051293] , [ 1206936000000 , 18.707820309008] , [ 1209528000000 , 17.459630929759] , [ 1212206400000 , 16.500616076782] , [ 1214798400000 , 18.086324003978] , [ 1217476800000 , 18.929464156259] , [ 1220155200000 , 18.233728682084] , [ 1222747200000 , 16.315776297325] , [ 1225425600000 , 14.632892190251] , [ 1228021200000 , 14.667835024479] , [ 1230699600000 , 13.946993947309] , [ 1233378000000 , 14.394304684398] , [ 1235797200000 , 13.724462792967] , [ 1238472000000 , 10.930879035807] , [ 1241064000000 , 9.8339915513708] , [ 1243742400000 , 10.053858541872] , [ 1246334400000 , 11.786998438286] , [ 1249012800000 , 11.780994901769] , [ 1251691200000 , 11.305889670277] , [ 1254283200000 , 10.918452290083] , [ 1256961600000 , 9.6811395055706] , [ 1259557200000 , 10.971529744038] , [ 1262235600000 , 13.330210480209] , [ 1264914000000 , 14.592637568961] , [ 1267333200000 , 14.605329141157] , [ 1270008000000 , 13.936853794037] , [ 1272600000000 , 12.189480759072] , [ 1275278400000 , 11.676151385046] , [ 1277870400000 , 13.058852800018] , [ 1280548800000 , 13.62891543203] , [ 1283227200000 , 13.811107569918] , [ 1285819200000 , 13.786494560786] , [ 1288497600000 , 14.045162857531] , [ 1291093200000 , 13.697412447286] , [ 1293771600000 , 13.677681376221] , [ 1296450000000 , 19.96151186453] , [ 1298869200000 , 21.049198298156] , [ 1301544000000 , 22.687631094009] , [ 1304136000000 , 25.469010617433] , [ 1306814400000 , 24.88379943712] , [ 1309406400000 , 24.203843814249] , [ 1312084800000 , 22.138760964036] , [ 1314763200000 , 16.034636966228] , [ 1317355200000 , 15.394958944555] , [ 1320033600000 , 12.62564246197] , [ 1322629200000 , 12.973735699739] , [ 1325307600000 , 15.78601833615] , [ 1327986000000 , 15.227368020134] , [ 1330491600000 , 15.899752650733] , [ 1333166400000 , 15.661317319168] , [ 1335758400000 , 15.359891177281]]
    } ,

    {
      "key" : "Europe" ,
      "values" : [ [ 1025409600000 , 9.3433263069351] , [ 1028088000000 , 8.4583069475546] , [ 1030766400000 , 8.0342398154196] , [ 1033358400000 , 8.1538966876572] , [ 1036040400000 , 10.743604786849] , [ 1038632400000 , 12.349366155851] , [ 1041310800000 , 10.742682503899] , [ 1043989200000 , 11.360983869935] , [ 1046408400000 , 11.441336039535] , [ 1049086800000 , 10.897508791837] , [ 1051675200000 , 11.469101547709] , [ 1054353600000 , 12.086311476742] , [ 1056945600000 , 8.0697180773504] , [ 1059624000000 , 8.2004392233445] , [ 1062302400000 , 8.4566434900643] , [ 1064894400000 , 7.9565760979059] , [ 1067576400000 , 9.3764619255827] , [ 1070168400000 , 9.0747664160538] , [ 1072846800000 , 10.508939004673] , [ 1075525200000 , 10.69936754483] , [ 1078030800000 , 10.681562399145] , [ 1080709200000 , 13.184786109406] , [ 1083297600000 , 12.668213052351] , [ 1085976000000 , 13.430509403986] , [ 1088568000000 , 12.393086349213] , [ 1091246400000 , 11.942374044842] , [ 1093924800000 , 12.062227685742] , [ 1096516800000 , 11.969974363623] , [ 1099195200000 , 12.14374574055] , [ 1101790800000 , 12.69422821995] , [ 1104469200000 , 9.1235211044692] , [ 1107147600000 , 8.758211757584] , [ 1109566800000 , 8.8072309258443] , [ 1112245200000 , 11.687595946835] , [ 1114833600000 , 11.079723082664] , [ 1117512000000 , 12.049712896076] , [ 1120104000000 , 10.725319428684] , [ 1122782400000 , 10.844849996286] , [ 1125460800000 , 10.833535488461] , [ 1128052800000 , 17.180932407865] , [ 1130734800000 , 15.894764896516] , [ 1133326800000 , 16.412751299498] , [ 1136005200000 , 12.573569093402] , [ 1138683600000 , 13.242301508051] , [ 1141102800000 , 12.863536342041] , [ 1143781200000 , 21.034044171629] , [ 1146369600000 , 21.419084618802] , [ 1149048000000 , 21.142678863692] , [ 1151640000000 , 26.56848967753] , [ 1154318400000 , 24.839144939906] , [ 1156996800000 , 25.456187462166] , [ 1159588800000 , 26.350164502825] , [ 1162270800000 , 26.478333205189] , [ 1164862800000 , 26.425979547846] , [ 1167541200000 , 28.191461582256] , [ 1170219600000 , 28.930307448808] , [ 1172638800000 , 29.521413891117] , [ 1175313600000 , 28.188285966466] , [ 1177905600000 , 27.704619625831] , [ 1180584000000 , 27.49086242483] , [ 1183176000000 , 28.770679721286] , [ 1185854400000 , 29.06048067145] , [ 1188532800000 , 28.240998844973] , [ 1191124800000 , 33.004893194128] , [ 1193803200000 , 34.075180359928] , [ 1196398800000 , 32.548560664834] , [ 1199077200000 , 30.629727432729] , [ 1201755600000 , 28.642858788159] , [ 1204261200000 , 27.973575227843] , [ 1206936000000 , 27.393351882726] , [ 1209528000000 , 28.476095288522] , [ 1212206400000 , 29.29667866426] , [ 1214798400000 , 29.222333802896] , [ 1217476800000 , 28.092966093842] , [ 1220155200000 , 28.107159262922] , [ 1222747200000 , 25.482974832099] , [ 1225425600000 , 21.208115993834] , [ 1228021200000 , 20.295043095268] , [ 1230699600000 , 15.925754618402] , [ 1233378000000 , 17.162864628346] , [ 1235797200000 , 17.084345773174] , [ 1238472000000 , 22.24600710228] , [ 1241064000000 , 24.530543998508] , [ 1243742400000 , 25.084184918241] , [ 1246334400000 , 16.606166527359] , [ 1249012800000 , 17.239620011628] , [ 1251691200000 , 17.336739127379] , [ 1254283200000 , 25.478492475754] , [ 1256961600000 , 23.017152085244] , [ 1259557200000 , 25.617745423684] , [ 1262235600000 , 24.061133998641] , [ 1264914000000 , 23.223933318646] , [ 1267333200000 , 24.425887263936] , [ 1270008000000 , 35.501471156693] , [ 1272600000000 , 33.775013878675] , [ 1275278400000 , 30.417993630285] , [ 1277870400000 , 30.023598978467] , [ 1280548800000 , 33.327519522436] , [ 1283227200000 , 31.963388450372] , [ 1285819200000 , 30.49896723209] , [ 1288497600000 , 32.403696817913] , [ 1291093200000 , 31.47736071922] , [ 1293771600000 , 31.53259666241] , [ 1296450000000 , 41.760282761548] , [ 1298869200000 , 45.605771243237] , [ 1301544000000 , 39.986557966215] , [ 1304136000000 , 43.84633051005] , [ 1306814400000 , 39.857316881858] , [ 1309406400000 , 37.675127768207] , [ 1312084800000 , 35.775077970313] , [ 1314763200000 , 48.631009702578] , [ 1317355200000 , 42.830831754505] , [ 1320033600000 , 35.611502589362] , [ 1322629200000 , 35.320136981738] , [ 1325307600000 , 31.564136901516] , [ 1327986000000 , 32.074407502433] , [ 1330491600000 , 35.053013769977] , [ 1333166400000 , 33.873085184128] , [ 1335758400000 , 32.321039427046]]
    } ,

    {
      "key" : "Australia" ,
      "values" : [ [ 1025409600000 , 5.1162447683392] , [ 1028088000000 , 4.2022848306513] , [ 1030766400000 , 4.3543715758736] , [ 1033358400000 , 5.4641223667245] , [ 1036040400000 , 6.0041275884577] , [ 1038632400000 , 6.6050520064486] , [ 1041310800000 , 5.0154059912793] , [ 1043989200000 , 5.1835708554647] , [ 1046408400000 , 5.1142682006164] , [ 1049086800000 , 5.0271381717695] , [ 1051675200000 , 5.3437782653456] , [ 1054353600000 , 5.2105844515767] , [ 1056945600000 , 6.552565997799] , [ 1059624000000 , 6.9873363581831] , [ 1062302400000 , 7.010986789097] , [ 1064894400000 , 4.4254242025515] , [ 1067576400000 , 4.9613848042174] , [ 1070168400000 , 4.8854920484764] , [ 1072846800000 , 4.0441111794228] , [ 1075525200000 , 4.0219596813179] , [ 1078030800000 , 4.3065749225355] , [ 1080709200000 , 3.9148434915404] , [ 1083297600000 , 3.8659430654512] , [ 1085976000000 , 3.9572824600686] , [ 1088568000000 , 4.7372190641522] , [ 1091246400000 , 4.6871476374455] , [ 1093924800000 , 5.0398702564196] , [ 1096516800000 , 5.5221787544964] , [ 1099195200000 , 5.424646299798] , [ 1101790800000 , 5.9240223067349] , [ 1104469200000 , 5.9936860983601] , [ 1107147600000 , 5.8499523215019] , [ 1109566800000 , 6.4149040329325] , [ 1112245200000 , 6.4547895561969] , [ 1114833600000 , 5.9385382611161] , [ 1117512000000 , 6.0486751030592] , [ 1120104000000 , 5.23108613838] , [ 1122782400000 , 5.5857797121029] , [ 1125460800000 , 5.3454665096987] , [ 1128052800000 , 5.0439154120119] , [ 1130734800000 , 5.054634702913] , [ 1133326800000 , 5.3819451380848] , [ 1136005200000 , 5.2638869269803] , [ 1138683600000 , 5.5806167415681] , [ 1141102800000 , 5.4539047069985] , [ 1143781200000 , 7.6728842432362] , [ 1146369600000 , 7.719946716654] , [ 1149048000000 , 8.0144619912942] , [ 1151640000000 , 7.942223133434] , [ 1154318400000 , 8.3998279827444] , [ 1156996800000 , 8.532324572605] , [ 1159588800000 , 4.7324285199763] , [ 1162270800000 , 4.7402397487697] , [ 1164862800000 , 4.9042069355168] , [ 1167541200000 , 5.9583963430882] , [ 1170219600000 , 6.3693899239171] , [ 1172638800000 , 6.261153903813] , [ 1175313600000 , 5.3443942184584] , [ 1177905600000 , 5.4932111235361] , [ 1180584000000 , 5.5747393101109] , [ 1183176000000 , 5.3833633060013] , [ 1185854400000 , 5.5125898831832] , [ 1188532800000 , 5.8116112661327] , [ 1191124800000 , 4.3962296939996] , [ 1193803200000 , 4.6967663605521] , [ 1196398800000 , 4.7963004350914] , [ 1199077200000 , 4.1817985183351] , [ 1201755600000 , 4.3797643870182] , [ 1204261200000 , 4.6966642197965] , [ 1206936000000 , 4.3609995132565] , [ 1209528000000 , 4.4736290996496] , [ 1212206400000 , 4.3749762738128] , [ 1214798400000 , 3.3274661194507] , [ 1217476800000 , 3.0316184691337] , [ 1220155200000 , 2.5718140204728] , [ 1222747200000 , 2.7034994044603] , [ 1225425600000 , 2.2033786591364] , [ 1228021200000 , 1.9850621240805] , [ 1230699600000 , 0] , [ 1233378000000 , 0] , [ 1235797200000 , 0] , [ 1238472000000 , 0] , [ 1241064000000 , 0] , [ 1243742400000 , 0] , [ 1246334400000 , 0] , [ 1249012800000 , 0] , [ 1251691200000 , 0] , [ 1254283200000 , 0.44495950017788] , [ 1256961600000 , 0.33945469262483] , [ 1259557200000 , 0.38348269455195] , [ 1262235600000 , 0] , [ 1264914000000 , 0] , [ 1267333200000 , 0] , [ 1270008000000 , 0] , [ 1272600000000 , 0] , [ 1275278400000 , 0] , [ 1277870400000 , 0] , [ 1280548800000 , 0] , [ 1283227200000 , 0] , [ 1285819200000 , 0] , [ 1288497600000 , 0] , [ 1291093200000 , 0] , [ 1293771600000 , 0] , [ 1296450000000 , 0.52216435716176] , [ 1298869200000 , 0.59275786698454] , [ 1301544000000 , 0] , [ 1304136000000 , 0] , [ 1306814400000 , 0] , [ 1309406400000 , 0] , [ 1312084800000 , 0] , [ 1314763200000 , 0] , [ 1317355200000 , 0] , [ 1320033600000 , 0] , [ 1322629200000 , 0] , [ 1325307600000 , 0] , [ 1327986000000 , 0] , [ 1330491600000 , 0] , [ 1333166400000 , 0] , [ 1335758400000 , 0]]
    } ,

    {
      "key" : "Antarctica" ,
      "values" : [ [ 1025409600000 , 1.3503144674343] , [ 1028088000000 , 1.2232741112434] , [ 1030766400000 , 1.3930470790784] , [ 1033358400000 , 1.2631275030593] , [ 1036040400000 , 1.5842699103708] , [ 1038632400000 , 1.9546996043116] , [ 1041310800000 , 0.8504048300986] , [ 1043989200000 , 0.85340686311353] , [ 1046408400000 , 0.843061357391] , [ 1049086800000 , 2.119846992476] , [ 1051675200000 , 2.5285382124858] , [ 1054353600000 , 2.5056570712835] , [ 1056945600000 , 2.5212789901005] , [ 1059624000000 , 2.6192011642534] , [ 1062302400000 , 2.5382187823805] , [ 1064894400000 , 2.3393223047168] , [ 1067576400000 , 2.491219888698] , [ 1070168400000 , 2.497555874906] , [ 1072846800000 , 1.734018115546] , [ 1075525200000 , 1.9307268299646] , [ 1078030800000 , 2.2261679836799] , [ 1080709200000 , 1.7608893704206] , [ 1083297600000 , 1.6242690616808] , [ 1085976000000 , 1.7161663801295] , [ 1088568000000 , 1.7183554537038] , [ 1091246400000 , 1.7179780759145] , [ 1093924800000 , 1.7314274801784] , [ 1096516800000 , 1.2596883356752] , [ 1099195200000 , 1.381177053009] , [ 1101790800000 , 1.4408819615814] , [ 1104469200000 , 3.4743581836444] , [ 1107147600000 , 3.3603749903192] , [ 1109566800000 , 3.5350883257893] , [ 1112245200000 , 3.0949644237828] , [ 1114833600000 , 3.0796455899995] , [ 1117512000000 , 3.3441247640644] , [ 1120104000000 , 4.0947643978168] , [ 1122782400000 , 4.4072631274052] , [ 1125460800000 , 4.4870979780825] , [ 1128052800000 , 4.8404549457934] , [ 1130734800000 , 4.8293016233697] , [ 1133326800000 , 5.2238093263952] , [ 1136005200000 , 3.382306337815] , [ 1138683600000 , 3.7056975170243] , [ 1141102800000 , 3.7561118692318] , [ 1143781200000 , 2.861913700854] , [ 1146369600000 , 2.9933744103381] , [ 1149048000000 , 2.7127537218463] , [ 1151640000000 , 3.1195497076283] , [ 1154318400000 , 3.4066964004508] , [ 1156996800000 , 3.3754571113569] , [ 1159588800000 , 2.2965579982924] , [ 1162270800000 , 2.4486818633018] , [ 1164862800000 , 2.4002308848517] , [ 1167541200000 , 1.9649579750349] , [ 1170219600000 , 1.9385263638056] , [ 1172638800000 , 1.9128975336387] , [ 1175313600000 , 2.3412869836298] , [ 1177905600000 , 2.4337870351445] , [ 1180584000000 , 2.62179703171] , [ 1183176000000 , 3.2642864957929] , [ 1185854400000 , 3.3200396223709] , [ 1188532800000 , 3.3934212707572] , [ 1191124800000 , 4.2822327088179] , [ 1193803200000 , 4.1474964228541] , [ 1196398800000 , 4.1477082879801] , [ 1199077200000 , 5.2947122916128] , [ 1201755600000 , 5.2919843508028] , [ 1204261200000 , 5.198978305031] , [ 1206936000000 , 3.5603057673513] , [ 1209528000000 , 3.3009087690692] , [ 1212206400000 , 3.1784852603792] , [ 1214798400000 , 4.5889503538868] , [ 1217476800000 , 4.401779617494] , [ 1220155200000 , 4.2208301828278] , [ 1222747200000 , 3.89396671475] , [ 1225425600000 , 3.0423832241354] , [ 1228021200000 , 3.135520611578] , [ 1230699600000 , 1.9631418164089] , [ 1233378000000 , 1.8963543874958] , [ 1235797200000 , 1.8266636017025] , [ 1238472000000 , 0.93136635895188] , [ 1241064000000 , 0.92737801918888] , [ 1243742400000 , 0.97591889805002] , [ 1246334400000 , 2.6841193805515] , [ 1249012800000 , 2.5664341140531] , [ 1251691200000 , 2.3887523699873] , [ 1254283200000 , 1.1737801663681] , [ 1256961600000 , 1.0953582317281] , [ 1259557200000 , 1.2495674976653] , [ 1262235600000 , 0.36607452464754] , [ 1264914000000 , 0.3548719047291] , [ 1267333200000 , 0.36769242398939] , [ 1270008000000 , 0] , [ 1272600000000 , 0] , [ 1275278400000 , 0] , [ 1277870400000 , 0] , [ 1280548800000 , 0] , [ 1283227200000 , 0] , [ 1285819200000 , 0.85450741275337] , [ 1288497600000 , 0.91360317921637] , [ 1291093200000 , 0.89647678692269] , [ 1293771600000 , 0.87800687192639] , [ 1296450000000 , 0] , [ 1298869200000 , 0] , [ 1301544000000 , 0.43668720882994] , [ 1304136000000 , 0.4756523602692] , [ 1306814400000 , 0.46947368328469] , [ 1309406400000 , 0.45138896152316] , [ 1312084800000 , 0.43828726648117] , [ 1314763200000 , 2.0820861395316] , [ 1317355200000 , 0.9364411075395] , [ 1320033600000 , 0.60583907839773] , [ 1322629200000 , 0.61096950747437] , [ 1325307600000 , 0] , [ 1327986000000 , 0] , [ 1330491600000 , 0] , [ 1333166400000 , 0] , [ 1335758400000 , 0]]
    }

    ]
}
function oochart_stackedarea_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
      var svg_d3 = oochart_create_svg(svg_id,svg);
      nv.addGraph(function() {
          var chart = nv.models.stackedAreaChart()
                        .x(function(d) { return d[0] })
                        .y(function(d) { return d[1] })
                        .clipEdge(true)
                        .useInteractiveGuideline(true)
                        ;
          if(simple){
                chart.showLegend(false).showControls(false).showXAxis(false).showYAxis(false);
            };
          chart.xAxis
              .showMaxMin(false)
              .tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });

          chart.yAxis
              .tickFormat(d3.format(',.2f'));

          svg_d3.datum(data)
              .transition().duration(duration)
              .call(chart);

          nv.utils.windowResize(chart.update);

          return chart;
      });
}

function oochart_line_example_data(){
  var sin = [],sin2 = [],
      cos = [];

  //Data is represented as an array of {x,y} pairs.
  for (var i = 0; i < 100; i++) {
    sin.push({x: i, y: Math.sin(i/10)});
    sin2.push({x: i, y: Math.sin(i/10) *0.25 + 0.5});
    cos.push({x: i, y: .5 * Math.cos(i/10)});
  }

  //Line chart data should be sent as an array of series objects.
  return [
    {
      values: sin,      //values - represents the array of {x,y} data points
      key: 'Sine Wave', //key  - the name of the series.
      color: '#ff7f0e'  //color - optional: choose your own line color.
    },
    {
      values: cos,
      key: 'Cosine Wave',
      color: '#2ca02c'
    },
    {
      values: sin2,
      key: 'Another sine wave',
      color: '#7777ff',
      area: true      //area - set to true if you want this line to turn into a filled area chart.
    }
  ];
}
function oochart_line_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
      var chart = nv.models.lineChart()
        .useInteractiveGuideline(true)
        ;
      if(simple){
            chart.showLegend(false).showControls(false).showXAxis(false).showYAxis(false);
        };
      chart.xAxis
        .axisLabel('Time (ms)')
        .tickFormat(d3.format(',r'))
        ;

      chart.yAxis
        .axisLabel('Voltage (v)')
        .tickFormat(d3.format('.02f'))
        ;

        if((typeof data) == 'string'){
            data = oochart_example_datas[data]();
        };

        svg_d3.datum(data)
        .transition().duration(duration)
        .call(chart)
        ;

      nv.utils.windowResize(chart.update);

      return chart;
    });
}

function oochart_scatterbubble_example_data(groups=4, points=40){

      var data = [],
          shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'],
          random = d3.random.normal();

      for (i = 0; i < groups; i++) {
        data.push({
          key: 'Group ' + i,
          values: []
        });

        for (j = 0; j < points; j++) {
          data[i].values.push({
            x: random()
          , y: random()
          , size: Math.random()
          //, shape: shapes[j % 6]
          });
        }
      }
      return data;
};
function oochart_scatterbubble_create(svg_id,data,svg=null,parent=null, duration=0,simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
      var chart = nv.models.scatterChart()
                    .showDistX(true)
                    .showDistY(true)
                    .color(d3.scale.category10().range());
      if(simple){
            chart.showLegend(false).showControls(false).showXAxis(false).showYAxis(false);
        };

      chart.xAxis.tickFormat(d3.format('.02f'));
      chart.yAxis.tickFormat(d3.format('.02f'));

      svg_d3.datum(data)
        .transition().duration(duration)
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
}

function oochart_multibar_example_data(){
    return stream_layers(3,10+Math.random()*100,.1).map(function(data, i) {
        return {
          key: 'Stream' + i,
          values: data
        };
    });
}
function oochart_multibar_create(svg_id,data,svg=null,parent=null, duration=0, simple=false){
    var svg_d3 = oochart_create_svg(svg_id,svg);
    nv.addGraph(function() {
        var chart = nv.models.multiBarChart();
        if(simple){
            chart.showLegend(false).showControls(false).showXAxis(false).showYAxis(false);
            chart.margin({top:0,right:0,bottom:0,left:0});
        };

        chart.xAxis
            .tickFormat(d3.format(',f'));

        chart.yAxis
            .tickFormat(d3.format(',.1f'));

        if((typeof data) == 'string'){
            data = oochart_example_datas[data]();
        };

        svg_d3.datum(data)
            .transition().duration(duration)
            .call(chart)
            ;

        nv.utils.windowResize(chart.update);

        return chart;
    }, function(){
        if(parent != null){
            let _$svg = $('#'+svg_id);
            if(svg != null){
                _$svg = $(svg);
            };
            /*
            if( simple){
                let buttons = _$svg.find('.nv-legendWrap');
                buttons.css('display','none');
            };*/
            $(parent).empty();
            _$svg.attr('viewBox','0 0 100 60')
            //$(parent).attr('width','100px')
            //$(parent).attr('height','70px')
            $(parent).append(_$svg);
        };
    });

}

var oochart_example_datas = {
    'linefinder': oochart_linefinder_example_data,
    'line': oochart_line_example_data,
    'multibar': oochart_multibar_example_data
}

function webpage_render(url, data, async=true){
    let data_post = [];
    let data_func = {};
    data.forEach(function(val,index,arr){
        data_post.push({'data':val.data, 'me':val.me});
        data_func[val.me] = {'that':val.that, 'func':val.func, 'trigger_event':val.trigger_event};
    })
    let data_j = null;
    try{
        data_j = JSON.stringify(data_post);
    }catch(err){
        let data_a = []
        data_post.forEach(function(val, index, arr){
            let val_j = JSON.stringify(val);
            data_a.push(val_j);
        })
        data_j = JSON.stringify(data_a)
    }
    $.ajaxSetup({'async': async})
    $.post(url, {'data':data_j}, function(response,status){
        let ret_data = response.data;
        if(ret_data != null && ret_data !== 'null' && ret_data !== 'undefined'){
            ret_data.forEach(function(val, index, arr){
                if(data_func[val.me].trigger_event == null || data_func[val.me].trigger_event === undefined){
                    data_func[val.me].func(that=data_func[val.me].that, val.data);
                }else{
                    data_func[val.me].func(that=data_func[val.me].that, val.data, trigger_event=data_func[val.me].trigger_event);
                }
            })
        }
    });
}

function web_img_val(that, data, trigger_event=false){
    console.log(that.attr('id'));
    console.log(data);
    that.attr('src', data);
}

function ootable_cell_render(data,type,row,meta){
    if(data.indexOf('render_img:')==0){
        return "<img width='100px' onload=webcomponent_draw_img(this,'60px') src='"+data.substr('render_img:'.length)+"'/>";
    };
    return data;
}

function ootable_get_rowinfo(tr){
    let data = $(tr).closest('table').DataTable().rows(tr).data();
    return data[0];
}
