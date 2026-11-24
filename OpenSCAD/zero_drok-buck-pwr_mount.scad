// Mount for a Pi Zero and a DROK buck converter
// Gregory A Sanders - Feb, 2025
//
// bs = base
bsx = 72;
bsy = 48;
bsz = 3;
// ps = power supply
psx = 63.6;
psy = 27.2;
psz = 1.8;
// mh = Pi mount hole spacing
mhx = 58;
mhy = 23;
// op = opening in base
opx = 52;
opy = 32;
opz = 10;

$fn=64;



module base(){
    difference(){
        cube([bsx,bsy,bsz]);
        translate([bsx/2,bsy/2,-1])
        cube([opx,opy,opz],true);
    }
}

module ps(){
    difference(){
        cube([psx+2,psy+3,10]);
        translate([-1,3,0])
        difference(){
            union(){
                translate([0,-.5,-0.5])
                cube([psx+4,psy-2,12]);
                translate([3,-1.5,7])
                cube([psx+2,psy,psz]);
            }
        }
    }
}

module picoscrew(){
    union(){
        cylinder(20,r=1.5);
    }
}

module pico(){
    picoscrew();
    translate([0,mhy,0])
    picoscrew();
    translate([mhx,mhy,0])
    picoscrew();
    translate([mhx,0,0])
    picoscrew();
}

difference(){
    union(){
        base();
        translate([4,8,0])
        ps();
    }
    union(){
        translate([bsx/2-mhx/2,4,-.5])
        pico();
        translate([bsx/2-mhx/2,(bsy-mhy)-4,-.5])
        pico();
    }
}
