// For a Pi Zero stack mount to wall.
// Gregory A Sanders - Mar, 2026
//
//

// ea = ears
eax = 10;
eay = 10;
eaz = 6;

// bs = base
bsx = 72;
bsy = 48;
bsz = 3;

// mh = Pi mount hole spacing
mhx = 58;
mhy = 23;

// op = opening in base
opx = 52;
opy = 32;
opz = 10;

$fn=64;
module hole1(){
    cylinder(h=20,r=2);
}

module base(){
    difference(){
        cube([bsx,bsy,bsz]);
        translate([bsx/2,bsy/2,-1])
        cube([opx,opy,opz],true);
    }
}

module wallMountEar(){
    difference(){
    cube([eax,eay,eaz]);
    translate([eax/2,eay/2,-1])
    #hole1();
    }
}

module wallMountEars(){
    translate([0,-eay,-3])
    wallMountEar();
    translate([bsx-eax,-eay,-3])
    wallMountEar();
    translate([bsx-eax,bsy,-3])
    wallMountEar();
    translate([0,bsy,-3])
    wallMountEar();

}

module zeroscrew(){
    union(){
        cylinder(20,r=1.5);
    }
}

module zero(){
    zeroscrew();
    translate([0,mhy,0])
    zeroscrew();
    translate([mhx,mhy,0])
    zeroscrew();
    translate([mhx,0,0])
    zeroscrew();
}

module final(){
    difference(){
        union(){
            base();
            wallMountEars();
        }
        union(){
            translate([bsx/2-mhx/2,4,-.5])
            zero();
            translate([bsx/2-mhx/2,(bsy-mhy)-4,-.5])
            zero();
        }
    }
}

module flat_no_ears(){
    difference(){
        base();
        translate([bsx/2-mhx/2,4,-.5])
        zero();
        translate([bsx/2-mhx/2,(bsy-mhy)-4,-.5])
        zero();
    }
}

// final();
flat_no_ears();