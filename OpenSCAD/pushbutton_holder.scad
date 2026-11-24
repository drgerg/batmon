// Momentary pushbutton holder for Pi 3 A+
// 
qsw = 3; // Quantity of switches
phs = 58; // Pi Hole Spacing 
phR = (3.5/2); //Screw hole Radius
slX = 6; // Width (X) of landing on standoff
pbsR = (7/2); // Pushbutton switch shaft radius
pbsB = 10; // Pushbutton base diameter
pbsO = 4; // Offset added to phR to get total width of landing
landingX = phR+pbsO;
landingY = landingX*2;
inc = ((slX+phs)/(qsw+1));
$fn = 48;


module base(){
    cube([slX,landingY,3]);
    translate([phs,0,0])
    cube([slX,landingY,3]);
    translate([0,landingY,0])
    cube([slX+phs,3,landingY]);
}

module holes(){
    translate([slX/2,slX/2,-1])
    cylinder(h=6,r=phR);
    translate([(slX/2)+phs,(slX/2),-1])
    cylinder(h=6,r=(3.5/2));
    rotate([90,0,0])
    for (h=[inc:inc:(inc*qsw)]) {
        translate([h,landingY/2,-(landingY+4)])
        cylinder(h=6,r=pbsR);
    }

}
echo((slX*2+phs));
echo(qsw+1);
echo(inc);

difference(){
base();
holes();
}

// holes();
