from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')
simIK = client.require('simIK')

class SysCall:
    def __init__(self):
        self.ikEnv = None
        self.ikGroup_undamped = None
        self.ikGroup_damped = None
        self.simJoints = []
        self.ikJoints = []
        self.ikBase = None
        self.ikTip = None
        self.ikTarget = None
        self.ikTarget_handle = sim.getObject('/robot_base/maniSphere/target')
        self.ikBase_handle   = sim.getObject('/robot_base')

    def sysCall_init(self):
        # Scene objects
        simBase = sim.getObject('/robot_base')
        simTip = sim.getObject('/robot_base/joint1/link1/joint2/link2/joint3/link3/joint4/link4/tip')
        simTarget = sim.getObject('/robot_base/maniSphere/target')

        # Create IK environment
        self.ikEnv = simIK.createEnvironment()
        self.ikGroup_undamped = simIK.createGroup(self.ikEnv)
        simIK.setGroupCalculation(self.ikEnv, self.ikGroup_undamped, simIK.method_pseudo_inverse, 0, 6)
        simIK.addElementFromScene(self.ikEnv, self.ikGroup_undamped, simBase, simTip, simTarget, simIK.constraint_pose)

        self.ikGroup_damped = simIK.createGroup(self.ikEnv)
        simIK.setGroupCalculation(self.ikEnv, self.ikGroup_damped, simIK.method_damped_least_squares, 1, 99)
        simIK.addElementFromScene(self.ikEnv, self.ikGroup_damped, simBase, simTip, simTarget, simIK.constraint_pose)

    def sysCall_actuation(self):
        # Sync target dummy with scene
        res, *_ = simIK.handleGroup(self.ikEnv, self.ikGroup_undamped, {'syncWorlds': True})
        if res != simIK.result_success:
            simIK.handleGroup(self.ikEnv, self.ikGroup_damped, {'syncWorlds': True})
            sim.addLog(sim.verbosity_scriptwarnings, "IK solver failed.")


# --- Run simulation ---
call = SysCall()
sim.setStepping(True)
sim.startSimulation()
call.sysCall_init()

while sim.getSimulationState() != sim.simulation_stopped:
    call.sysCall_actuation()
    sim.step()

sim.stopSimulation()