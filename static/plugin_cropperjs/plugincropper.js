$(document).ready(function() {

    $(".image-cropper-container").each(function(){

        var options = $(this).data();

        var name = options.name;
        delete options.name;

        var cropper = null;

        $("input[data-cropper='cropper-"+name+"']").change(function() {


            if (this.files && this.files[0]) {
                var reader = new FileReader();

                reader.readAsDataURL(this.files[0]);

                reader.onload = function(oFREvent){
                    document.getElementById("cropper-img-"+name).src = oFREvent.target.result;
                    if (cropper){
                        cropper.replace(oFREvent.target.result);
                    } else {
                        cropper = setCropper(name, options);
                    }
                };
            }
        });

    });

    function setCropper(name, options) {
        var image = document.getElementById('cropper-img-'+name);
        try {
            console.log("akak", $(image).cropper());
        } catch (err){

        }

        options.crop = function (e) {
            $("#"+name+"_cropper_detail_x").val(e.detail.x);
            $("#"+name+"_cropper_detail_y").val(e.detail.y);
            $("#"+name+"_cropper_detail_width").val(e.detail.width);
            $("#"+name+"_cropper_detail_height").val(e.detail.height);
            $("#"+name+"_cropper_detail_rotate").val(e.detail.rotate);
            $("#"+name+"_cropper_detail_scaleX").val(e.detail.scaleX);
            $("#"+name+"_cropper_detail_scaleY").val(e.detail.scaleY);
        };

        return new Cropper(image, options);
    }

});