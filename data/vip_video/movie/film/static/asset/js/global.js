var MAC={
	'Image':{
		'Show': function(){
			$(".fed-lazy").lazyload({
				effect: "fadeIn",
				threshold: 200,
				failurelimit: 15,
				skip_invisible: false
			});
		},
    },
	'PageGo':{
        'Init':function() {
            $('.fed-page-jump').click(function () {
                var that =$(this);
                var url = that.attr('data-url');
                var total = parseInt(that.attr('data-total'));
                var sp = that.attr('data-sp');
                var page= parseInt($('#page').val());

                if(page>0&&(page<=total)){
                    // url=url.replace(sp + 'PAGELINK',sp + page).replace('PAGELINK',page);
                    url=url + page;
                    location.href=url;
                }
                return false;
            });
        }
    },
    'Cookie': {
        'Set': function(name,value,days){
            var exp = new Date();
            exp.setTime(exp.getTime() + days*24*60*60*1000);
            var arr=document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
            document.cookie=name+"="+encodeURIComponent(value)+";path=/;expires="+exp.toUTCString();
        },
        'Get': function(name){
            var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
            if(arr != null){ return decodeURIComponent(arr[2]); return null; }
        },
        'Del': function(name){
            var exp = new Date();
            exp.setTime(exp.getTime()-1);
            var cval = this.Get(name);
            if(cval != null){ document.cookie = name+"="+encodeURIComponent(cval)+";path=/;expires="+exp.toUTCString(); }
        }
    },
    'History': {
        'BoxShow':0,
        'Limit':10,
        'Days':7,
        'Json':'',
        'Init':function(){
            if($('.mac_history').length ==0){
                return;
            }

            $('.mac_history').hover(function(e){
                $('.mac_history_box').show();
            }, function(){
                $('.mac_history_box').hover(function(){
                    MAC.History.BoxShow=1;
                }, function(){
                    MAC.History.BoxShow=0;
                    $('.mac_history_box').hide();
                });
            });

            var jsondata = [];
            if(this.Json){
                jsondata = this.Json;
            }else{
                var jsonstr = MAC.Cookie.Get('mac_history');
                if(jsonstr != undefined){
                    jsondata = eval(jsonstr);
                }
            }

            html = '<dl class="mac_drop_box mac_history_box" style="display:none;">';
            html +='<dt><a target="_self" href="javascript:void(0)" onclick="MAC.History.Clear();">清空</a></dt>';

            if(jsondata.length > 0){
                for($i=0; $i<jsondata.length; $i++){
                    if($i%2==1){
                        html +='<dd class="odd">';
                    }else{
                        html +='<dd class="even">';
                    }
                    html +='<a href="'+jsondata[$i].link+'" class="hx_title">'+jsondata[$i].name+'</a></dd>';
                }
            }else{
                html +='<dd class="hide">暂无浏览记录</dd>';
            }
            html += '</dl>';

            $('.mac_history').after(html);
            var h = $('.mac_history').height();
            var position = $('.mac_history').position();
            $('.mac_history_box').css({'left':position.left,'top':(position.top+h)});


            if($(".mac_history_set").attr('data-name')){
                var $that = $(".mac_history_set");
                MAC.History.Set($that.attr('data-name'),$that.attr('data-link'),$that.attr('data-pic'));
            }
        },
        'Set':function(name,link,pic){
            if(!link){ link = document.URL; }
            var jsondata = MAC.Cookie.Get('mac_history');

            if(jsondata != undefined){
                this.Json = eval(jsondata);

                for($i=0;$i<this.Json.length;$i++){
                    if(this.Json[$i].link == link){
                        return false;
                    }
                }

                jsonstr = '{log:[{"name":"'+name+'","link":"'+link+'","pic":"'+pic+'"},';
                for($i=0; $i<this.Json.length; $i++){
                    if($i<= this.Limit && this.Json[$i]){
                        jsonstr += '{"name":"'+this.Json[$i].name+'","link":"'+this.Json[$i].link+'","pic":"'+this.Json[$i].pic+'"},';
                    }else{
                        break;
                    }
                }
                jsonstr = jsonstr.substring(0,jsonstr.lastIndexOf(','));
                jsonstr += "]}";
            }else{
                jsonstr = '{log:[{"name":"'+name+'","link":"'+link+'","pic":"'+pic+'"}]}';
            }
            this.Json = eval(jsonstr);
            MAC.Cookie.Set('mac_history',jsonstr,this.Days);
        },
        'Clear': function(){
            MAC.Cookie.Del('mac_history');
            $('.mac_history_box').html('<li class="hx_clear">已清空观看记录。</li>');
        },
    },

};

$(function(){
    //异步加载图片初始化
    MAC.Image.Show();
    //分页跳转初始化
    MAC.PageGo.Init();
    //历史记录初始化
    MAC.History.Init();
});
