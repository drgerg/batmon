// zero_arch_base_stand.scad 
// Side mount legs for my Pi Zero mount.
// Gregory A Sanders - March, 2025
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
opx = 62;
opy = 30;
opz = 20;
// ap = arch parameters
apy = bsy + 6;
aph = 6;

$fn=240;

module base(){
    difference(){
        cube([18,bsy,bsz]);
        translate([opx/2+aph,bsy/2,-1])
        cube([opx,opy,opz],true);
    }
}

module picoscrew(){
        cylinder(20,r=1.5);
}

module legholes(){
    union(){
        translate([bsx/2-mhx/2,4,-.5])
        picoscrew();
        translate([bsx/2-mhx/2,bsy-4,-.5])
        picoscrew();
    }
}

module stand(){
    difference(){
        translate([-aph,0,0])
            base();
        legholes();
    }
}

module side(){
    rotate([0,90,0])
        linear_extrude(height = aph) 
            difference(){
                circle(d=apy);
                union(){
                circle(d=apy-12);
                translate([0,-(apy/2+1)])
                square(apy+2);
                }
            }
}

side();
translate([aph,-bsy/2,0])
stand();
translate([0,apy/2-6,-10])
cube([6,6,10]);
translate([0,-apy/2,-10])
cube([6,6,10]);
