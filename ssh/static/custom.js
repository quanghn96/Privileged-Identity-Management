$(document).ready(function(){
 
    var idSSH;
    $(".btn.btn-success.viewUser").click(function(){
    	var id = this.id;
        idSSH = this.id;
        $.ajax({
        	url:'/ssh/ajax/get_User/',
        	data:{
        		'id':id
        	},
        	dataType: 'json',
        	success: function(data){
                var obj = jQuery.parseJSON(data);
                var a ="";
                $(obj).each(function(i, item){
                    a+="<tr><th>"+item.fields.username+"</th>" + "<th>"+"<button type=\"button\" id="+item.pk+" class=\"btn btn-danger deleteUser\">Delete</button>"+"</th></tr>";
                })
                $("#DisplayUser").html(a)
        	}
        });
    });
    $(document).on("click", ".btn.btn-danger.deleteUser", function(event){
        var idUser = this.id; 
        $.ajax({
            url:'/ssh/ajax/delete_User/',
            data:{
                'idUser':idUser,
                'idSSH':idSSH
            },
            dataType: 'json',
            success: function(data){
                if(data.id){
                    alert('fail');
                }
                else {
                    var obj = jQuery.parseJSON(data);
                    var a ="";
                    $(obj).each(function(i, item){
                        a+="<tr><th>"+item.fields.username+"</th>" + "<th>"+"<button type=\"button\" id="+item.pk+" class=\"btn btn-danger deleteUser\">Delete</button>"+"</th></tr>";
                    })
                    $("#DisplayUser").html(a)
                }
            }
        }); 
    });
    $('.addUser').click(function(){
        idSSH = this.id;
        $("#msg").html('');
    });
    $(document).on("click", ".btn.btn-primary.SaveUser", function(event){
        
        var username = $("#usr").val();
        $('#usr').val('');
        if(username==''){
            $("#msg").html('Username must be filled');
        } else{
            $("#msg").html('');
            $.ajax({
            url:'/ssh/ajax/add_User/',
            data:{
                'username':username,
                'idSSH':idSSH
            },
            dataType: 'json',
            success: function(data){
                if(data.id){
                    $("#msg").html(data.id);
                }
                
            }
        });
        }
    });
    $('.checkBlackList').click(function(){
        idSSH = this.id;
        $('#startTime').val('');
        $('#endTime').val('');
        $("#select").attr("selected",true);
    });
    var selectedCommand=0;
    $("select.command").change(function(){
        selectedCommand = $(this).children("option:selected").val();
        $.ajax({
            url:'/ssh/ajax/getTimeCommand/',
            data:{
                'idSSH':idSSH,
                'selectedCommand':selectedCommand
            },
            dataType:'json',
            success: function(data){
                if(data.id!='Fail'){
                    var obj = jQuery.parseJSON(data);console.log(obj.pk); 
                    $(obj).each(function(i, item){
                        $('#startTime').val(item.fields.startTime);
                        $('#endTime').val(item.fields.endTime);
                    })
                }else {
                    $('#startTime').val('');
                    $('#endTime').val('');
                }
            }
        })
    });
    $(".btn.btn-primary.SaveTime").click(function(){
        start = $('#startTime').val();
        end = $('#endTime').val();

        if(start.trim()!=null && end.trim()!=null){
            $.ajax({
                url:'/ssh/ajax/setTimeCommand/',
                data:{
                    'idSSH':idSSH,
                    'startTime':start,
                    'endTime':end,
                    'selectedCommand':selectedCommand
                },
                dataType:'json',
                success: function(data){
                    
                    if(data.id=="Fail"){
                        $("#err-message-cmd").text("");
                        $("#err-message-cmd").text("Save fail !");
                        $("#err-message-cmd").show();
                    }
                    else {
                        $("#err-message-cmd").text("");
                        $("#err-message-cmd").text("Successful!");
                        $("#err-message-cmd").show();
                    }
                }
            })
        }
    });
    /*$('.viewLog').click(function(){
        idSSH = this.id;
        $.ajax({
            url:'/ssh/ajax/viewLog',
            data:{
                'idSSH':idSSH
            },
            dataType:'json',
            success: function(data){
                var obj = jQuery.parseJSON(data);
                var a ="";
                $(obj).each(function(i, item){
                    a+=('<option id=\"'+item.pk+'\">'+item.fields.username+'</option>');
                })
                $('.logSSH').html('<div class="container"> <div class="col-md-2">Select User<br> </div><div class="col-md-1"><select class="vlog"><option disabled selected value id="select"> -- select an option -- </option>'+a+'   </select></div> <div class="col-md-1"> </div><button type=\"button\" class=\"btn btn-success OKLOG\">OK</button></div>         ');  
                $("select.vlog").change(function(){
                    logID = $(this).children("option:selected").attr('id');
                    $('.OKLOG').click(function(){
                        console.log(logID);
                        $.ajax({
                            url:'/ssh/ajax/viewLogUser',
                            data:{
                                'idSSH':idSSH,
                                'idUser':logID
                            },
                            dataType:'json',
                            success: function(data){
                                
                                var obj = jQuery.parseJSON(data);
                                var b = "";
                                $(obj).each(function(i,item){
                                    console.log(item);
                                })
                            }
                        });
                        $(".logSSH").html('');
                    })
                })  
            }
        });
        
        
    });
   */
    $("select.vlog").change(function(){
        logID = $(this).children("option:selected").val();
        console.log(logID);
        var idSSH = window.location.pathname.split('/')[3];
        console.log(idSSH) ;
        $.ajax({
            url:'/ssh/ajax/viewLogUser',
            data:{
                'idSSH':idSSH,
                'idUser':logID
            },
            dataType:'json',
            success: function(data){
                var obj = jQuery.parseJSON(data);
                var b = "";
                var c= "";
                $(obj).each(function(i,item){
                    var time = item.fields.logTime.split('T');
                    var str = item.fields.command.split('||||');
                    var cmd='';
                    
                    for(var j=0; j< str.length;j++){
                        cmd+=(str[j]+'<br>')
                    }
                    c = '<p><button class=\"btn btn-primary\" type=\"button\" data-toggle=\"collapse\" data-target=\"#'+item.pk+'\" aria-expanded=\"false\" aria-controls=\"collapseExample\">Button with data-target</button></p><div class=\"collapse\" id=\"'+item.pk+'\"><div class=\"card card-body\">'+cmd+'</div>';
                    b+=('<tr><td>'+time[0]+'</td><td>'+time[1].split('.')[0]+'</td><td>'+c+'</td></tr>');console.log(c);
                });
                $(".showLogSSH").html(b);
            }
        });
    });

    $("select.locationTicket").change(function(){
        var idLocation = $(this).children("option:selected").attr('id');
        $("#sendTicket").click(function(){
            console.log('data');
            var title = $("#titleTicket").val();            
            var value = $('#textTicket').val();
            var idUSer = $('.container.Ticket').attr('id');
            if(value.trim()!=''){console.log(idUSer);
                $.ajax({
                    url:'/ajax/ticket',
                    data:{
                        'idLocation':idLocation,
                        'message':value,
                        'idUSer':idUSer,
                        'title':title
                    },
                    dataType:'json',
                    success: function(data){
                        console.log(data);
                        if(data.id=='OK'){
                            $('.container.Ticket .row').remove();
                            $('.container.Ticket').html('<div style="color:red;">Send Ticket Successfully</div>');
                        }
                    }
                });
            }
        });
    });

    $('#AddConnectionBtn').click(function(){ 
        $('#ip').val('') ;
        $('#port').val('');
        $('#username').val('');
        $('#pass').val('');
    });

    $(".SaveConnection").click(function(){
        var ip = $('#ip').val();
        var port = $('#port').val();
        var username = $('#username').val();
        var pass = $('#pass').val();
        var idLoc = $("option:selected").attr('id');
        if(ip==null || port==null || username==null || pass==null){
            alert('Values are empty');
        }else {console.log(ip+' '+port+' '+username+' '+pass);
            $.ajax({
                url:'/ssh/ajax/addconnection',
                data:{
                    'ip':ip,
                    'port':port,
                    'username':username,
                    'pass':pass,
                    'idLoc':idLoc
                },
                dataType:'json',
                success: function(data){
                    if(data.id=="OK"){
                        $('.ctnaddConnection').html('<div style="color:red;">Create Successfully</div>');
                        $('.SaveConnection').hide();
                    }else {
                        $('.errormessageAdd').html('<div style="color:red;">Fail</div>');
                    }
                }
            });
        }

    });

    $(".DeleteConnection").click(function(){
        var id = this.id;
        $.ajax({
            url:'/ssh/ajax/DeleteConnection',
            data:{
                'id':id
            },
            dataType:'json',
            success: function(data){
                alert(data.id);
            }
        });
    });
    $('.EditConnection').click(function(){
        var Code = $('.ctnaddConnection').html();
        $('.ctnaddConnection').html('');
        var id = this.id;
        $('#ip1').val('') ;
        $('#port1').val('');
        $('#username1').val('');
        $('#pass1').val('');
        $.ajax({
            url:'/ssh/ajax/EditConnection',
            data:{
                'id':id
            },
            dataType:'json',
            success: function(data){console.log(data);
                var obj = jQuery.parseJSON(data);
                var b = "";
                $(obj).each(function(i,item){
                   console.log(item.fields);
                   $("#ip1").val(item.fields.ip);
                   $("#port1").val(item.fields.port);
                   $("#username1").val(item.fields.username);

                })
            }
        });
        $(".SaveEditConnection").click(function(){
                        var ip = $('#ip1').val();
                        var port = $('#port1').val();
                        var username = $('#username1').val();
                        var pass = $('#pass1').val();
                        var idLoc = $("option:selected").attr('id');
                        if(ip == '' || port == '' || username == '' || pass.trim() == ''){
                            
                        } 
                        else {
                            $.ajax({
                                url:'/ssh/ajax/SaveEditConnection',
                                data:{
                                    'id':id,
                                    'ip':ip,
                                    'port':port,
                                    'username':username,
                                    'pass':pass,
                                    'idLoc':idLoc
                                },
                                dataType:'json',
                                success: function(data){
                                    if(data.id=="OK"){
                                        $('.ctnEditConnection').html('<div style="color:red;">Edit Successfully</div>');
                                        $('.SaveEditConnection').hide();
                                        $('.ctnaddConnection').html(Code);
                                    }else {
                                        $('.errormessageAdd').html('<div style="color:red;">Fail</div>');
                                    }
                                }
                            });
                        }
                   });
    });

//[{"model": "ssh.ssh", "pk": 4, "fields": {"port": 22, "username": "root"}}]

    $(".ViewTicket").click(function(){
        var id = this.id;
        $.ajax({
            url:'/ajax/viewTicket',
            data:{
                'id':id
            },
            dataType:'json',
            success: function(data){
              $(".Ticket").html('');
               console.log(data);
            }
        });
    });

    $(".sendMessageAdmin").click(function(){
        var idTicket = window.location.pathname.split('/')[2];
        var message = $("#messageText").val();
        $.ajax({
            url:'/ajax/AddMessage',
            data:{
                'idTicket':idTicket,
                'message':message
            },
            dataType:'json',
            success: function(data){
                if(data.id=="OK") alert('Send message OK');
            }
        });
    });


});