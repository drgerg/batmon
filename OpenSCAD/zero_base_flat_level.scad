// zero_base_flat_level.scad - a flat rectangular level for stacking Pi Zeros.
// mod of Garbage_Mount_Amp_Level.scad
// 2025 - dr.gerg@drgerg.com

pidims=[65,30,3];
$fn=48;

module hole1(){
    cylinder(h=10,r=1.6);
}

module stand(){
    cube([7,4,8],true);
}

// 
// offsetx,offsety,holespacex,holespacey
//
module drillholes(ofx,ofy,hsx,hsy){
    translate([ofx,ofy,-1])
    hole1();
    translate([ofx+hsx,ofy,-1])
    hole1();
    translate([ofx+hsx,ofy+hsy,-1])
    hole1();
    translate([ofx,ofy+hsy,-1])
    hole1();
}

// 
// offsetx,offsety,secholespacex,secholespacey
//
module secondholes(ofx,ofy,ssx,ssy){
    translate([ofx,ofy,-1])
    hole1();
    translate([ofx+ssx,ofy,-1])
    hole1();
    translate([ofx+ssx,ofy+ssy,-1])
    hole1();
    translate([ofx,ofy+ssy,-1])
    hole1();
}


module pibase(){
    translate([0,15,7])
    legpair();
    translate([0,-(pidims[1]/2)-1,19.5+(pidims[2]/2)])
    difference(){
        cube(pidims,true);
        union(){
            translate([-pidims[0]/2,-pidims[1]/2,-pidims[2]/2])
            drillholes(3.5,3.5,48.5,57.5);
            cube([pidims[0]-14,pidims[1]-14,9],true);
        }
    }
}

module amp_level(){
        difference(){
            cube(pidims,true);
            union(){
                translate([-pidims[0]/2,-pidims[1]/2,-pidims[2]/2])
                #drillholes(3.5,3.5,58,23);
                // translate([-pidims[0]/2,-pidims[1]/2,-pidims[2]/2])
                // secondholes(3.5,3.5,49,57.5-25);
                cube([pidims[0]-14,pidims[1]-14,9],true);
            }
        }
    
}

amp_level();

