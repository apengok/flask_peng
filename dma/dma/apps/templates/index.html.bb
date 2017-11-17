{% extends "base.html" %}

{% block title %}DMA |Index {{ title }}{% endblock %}

<!-- head -->
{% block head %}
    {{ super() }}
    <link href="{{ url_for('static',filename='css/wbalance.css') }}" rel="stylesheet">
    
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=1.5&ak=1a63afc62e06c2d3a54b3ebc9e3f6822"></script>
    

 <style>
      body{
        text-align:center;
      }
      #ctrl{
        width: 500px;
        margin:0 auto;
      }
      .gmap3{
        margin: 20px auto;
        border: 1px dashed #C0C0C0;
        width: 500px;
        height: 400px;
      }
    </style>



{% endblock %}

{% block content %}

    <h2>map example</h2>
    <div id="ctrl">Address : <input type="text" id="test-address" size="60"> <input type="button" id="testok" value="Ok" /></div>
    <div id="test" class="gmap3" style=" margin: 20px auto;border: 1px dashed #C0C0C0;width: 500px;height: 400px;"></div>
    Fill in an address, a marker will be added and the map will be centered on it
    <div><span>经度：</span><input id="jd" /><span>纬度：</span><input id="wd" /></div>
    <script type="text/javascript">
        var map = new BMap.Map("test");
        var marker = null;

        var initialize = function(lng,lat){
            var point = new BMap.Point(lng,lat);
            map.centerAndZoom(point, 16); //设置中心坐标和缩放比例
            map.clearOverlays();
            marker = new BMap.Marker(point);  // 创建标注
            map.addOverlay(marker);              // 将标注添加到地图中
            marker.enableDragging();    //可拖拽
            marker.enableMassClear(); //允许覆盖物在map.clearOverlays方法中被清除。
            marker.addEventListener("dragend",function(){
                var p = marker.getPosition();
                map.centerAndZoom(p, 16);
                $("#jd").val(p.lng);
                $("#wd").val(p.lat);
            });
        };
        initialize(113.3148,23.135311);

        map.addControl(new BMap.NavigationControl());  //添加默认缩放平移控件
        map.enableScrollWheelZoom();    //启用滚轮放大缩小，默认禁用

        /*
        map.addEventListener("dragend", function showInfo(){
            var cp = map.getCenter();
            $("#jd").val(cp.lng);
            $("#wd").val(cp.lat);
        });
        */

        function searchAddr(addr){
            var geocoder = new BMap.Geocoder();
            geocoder.getPoint(addr,function(point){
                if(point){
                    $("#jd").val(point.lng);
                    $("#wd").val(point.lat);
                    initialize(point.lng,point.lat);
                }
            });
        }

        var searchS =  function(){
            var addr = $('#test-address').val();
            if ( !addr || !addr.length ) return;
            searchAddr(addr);
        };

        $('#testok').bind('click',function(){
            searchS();
        });

        $('#test-address').keypress(function(e){
            if (e.keyCode == 13){
                searchS();
            }
        });

    </script>
{% endblock %}

