//
//  AccelerometerInterfaceController.swift
//  watchOS2Sampler
//
//  Created by Shuichi Tsutsumi on 2015/06/13.
//  Copyright © 2015 Shuichi Tsutsumi. All rights reserved.
//
import WatchKit
import Foundation
import CoreMotion


class AccelerometerInterfaceController: WKInterfaceController{

    
    @IBOutlet weak var labelX: WKInterfaceLabel!
    @IBOutlet weak var labelY: WKInterfaceLabel!
    @IBOutlet weak var labelZ: WKInterfaceLabel!
    
    let motionManager = CMMotionManager()
    
    var bufAccel :[Double] = []
    
    var isStarted :Bool = false;
    
    @IBOutlet weak var btnStart: WKInterfaceButton!
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        
        motionManager.accelerometerUpdateInterval = 0.1
    }

    override func willActivate() {
        super.willActivate()

        if motionManager.isAccelerometerAvailable {
            let handler:CMAccelerometerHandler = {(data: CMAccelerometerData?, error: Error?) -> Void in
                
                if(self.isStarted) {
                    self.bufAccel.append(data!.acceleration.x)
                    self.bufAccel.append(data!.acceleration.y)
                    self.bufAccel.append(data!.acceleration.z)
                }
            }
            motionManager.startAccelerometerUpdates(to: OperationQueue.current!, withHandler: handler)
        }
        else {
            print("acclerometer not available")
        }
    }

    override func didDeactivate() {
        super.didDeactivate()
        
        motionManager.stopAccelerometerUpdates()
    }
    
    @IBAction func tapRecognized(_ sender: AnyObject) {
        if(isStarted) {
            btnStart.setTitle("Start")
            print(self.bufAccel)
            bufAccel = []
            print("stopped")
        } else {
            btnStart.setTitle("Stop")
            print("started")
        }
        isStarted = !isStarted
    }
    
}
