//
//  FaceOff.swift
//  FaceOff WatchKit Extension
//
//  Created by Xiang 'Anthony' Chen on 3/25/20.
//  Copyright © 2020 Xiang 'Anthony' Chen. All rights reserved.
//

import WatchKit
import Foundation
import CoreMotion

class FaceOff: WKInterfaceController{
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
    }
    
    override func willActivate() {
        super.willActivate()
    }
    
    override func didDeactivate() {
        super.didDeactivate()
    }
    
    // get ms value of the current time
    static  func getCurrentMillis()->Int64{
        return Int64(NSDate().timeIntervalSince1970 * 1000)
    }
}
