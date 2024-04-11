
import struct


MAX_SHARED_DATA = 10

class RobotData:
    def __init__(self):
        self.header = b''
        self.time = 0.0
        self.jnt_ref = [0.0] * 6
        self.jnt_ang = [0.0] * 6
        self.jnt_cur = [0.0] * 6
        self.tcp_ref = [0.0] * 6
        self.tcp_pos = [0.0] * 6
        self.analog_in = [0.0] * 4
        self.analog_out = [0.0] * 4
        self.digital_in = [0] * 16
        self.digital_out = [0] * 16
        self.jnt_temperature = [0.0] * 6
        self.task_pc = 0
        self.task_repeat = 0
        self.task_run_id = 0
        self.task_run_num = 0
        self.task_run_time = 0
        self.task_state = 0
        self.default_speed = 0.0
        self.robot_state = 0
        self.information_chunk_1 = 0
        self.reserved_1 = [0.0] * 6
        self.jnt_info = [0] * 6
        self.collision_detect_onoff = 0
        self.is_freedrive_mode = 0
        self.real_vs_simulation_mode = 0
        self.init_state_info = 0
        self.init_error = 0
        self.tfb_analog_in = [0.0] * 2
        self.tfb_digital_in = [0] * 2
        self.tfb_digital_out = [0] * 2
        self.tfb_voltage_out = 0.0
        self.op_stat_collision_occur = 0
        self.op_stat_sos_flag = 0
        self.op_stat_self_collision = 0
        self.op_stat_soft_estop_occur = 0
        self.op_stat_ems_flag = 0
        self.information_chunk_2 = 0
        self.information_chunk_3 = 0
        self.inbox_trap_flag = [0] * 2
        self.inbox_check_mode = [0] * 2
        self.eft_fx = 0.0
        self.eft_fy = 0.0
        self.eft_fz = 0.0
        self.eft_mx = 0.0
        self.eft_my = 0.0
        self.eft_mz = 0.0
        self.information_chunk_4 = 0
        self.extend_io1_analog_in = [0.0] * 4
        self.extend_io1_analog_out = [0.0] * 4
        self.extend_io1_digital_info = 0
        self.aa_joint_ref = [0.0] * 6
        self.safety_board_stat_info = 0
        self.fdata = [0.0] * MAX_SHARED_DATA
        self.idata = [0] * MAX_SHARED_DATA

    def pack(self):
        data = b''.join([
            self.header,
            struct.pack('f', self.time),
            *[struct.pack('f', x) for x in self.jnt_ref],
            *[struct.pack('f', x) for x in self.jnt_ang],
            *[struct.pack('f', x) for x in self.jnt_cur],
            *[struct.pack('f', x) for x in self.tcp_ref],
            *[struct.pack('f', x) for x in self.tcp_pos],
            *[struct.pack('f', x) for x in self.analog_in],
            *[struct.pack('f', x) for x in self.analog_out],
            *[struct.pack('i', x) for x in self.digital_in],
            *[struct.pack('i', x) for x in self.digital_out],
            *[struct.pack('f', x) for x in self.jnt_temperature],
            struct.pack('i', self.task_pc),
            struct.pack('i', self.task_repeat),
            struct.pack('i', self.task_run_id),
            struct.pack('i', self.task_run_num),
            struct.pack('i', self.task_run_time),
            struct.pack('i', self.task_state),
            struct.pack('f', self.default_speed),
            struct.pack('i', self.robot_state),
            struct.pack('i', self.information_chunk_1),
            *[struct.pack('f', x) for x in self.reserved_1],
            *[struct.pack('i', x) for x in self.jnt_info],
            struct.pack('i', self.collision_detect_onoff),
            struct.pack('i', self.is_freedrive_mode),
            struct.pack('i', self.real_vs_simulation_mode),
            struct.pack('i', self.init_state_info),
            struct.pack('i', self.init_error),
            *[struct.pack('f', x) for x in self.tfb_analog_in],
            *[struct.pack('i', x) for x in self.tfb_digital_in],
            *[struct.pack('i', x) for x in self.tfb_digital_out],
            struct.pack('f', self.tfb_voltage_out),
            struct.pack('i', self.op_stat_collision_occur),
            struct.pack('i', self.op_stat_sos_flag),
            struct.pack('i', self.op_stat_self_collision),
            struct.pack('i', self.op_stat_soft_estop_occur),
            struct.pack('i', self.op_stat_ems_flag),
            struct.pack('i', self.information_chunk_2),
            struct.pack('i', self.information_chunk_3),
            *[struct.pack('i', x) for x in self.inbox_trap_flag],
            *[struct.pack('i', x) for x in self.inbox_check_mode],
            struct.pack('f', self.eft_fx),
            struct.pack('f', self.eft_fy),
            struct.pack('f', self.eft_fz),
            struct.pack('f', self.eft_mx),
            struct.pack('f', self.eft_my),
            struct.pack('f', self.eft_mz),
            struct.pack('i', self.information_chunk_4),
            *[struct.pack('f', x) for x in self.extend_io1_analog_in],
            *[struct.pack('f', x) for x in self.extend_io1_analog_out],
            struct.pack('I', self.extend_io1_digital_info),
            *[struct.pack('f', x) for x in self.aa_joint_ref],
            struct.pack('I', self.safety_board_stat_info),
            *[struct.pack('f', x) for x in self.fdata],
            *[struct.pack('i', x) for x in self.idata]
        ])
        return data

    def unpack(self, data):
        offset = 0
        self.header = struct.unpack('4s', data[offset:offset+4])
        offset += 4
        self.time, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.jnt_ref = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.jnt_ang = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.jnt_cur = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.tcp_ref = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.tcp_pos = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.analog_in = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(4)]
        offset += 16
        self.analog_out = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(4)]
        offset += 16
        self.digital_in = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(16)]
        offset += 64
        self.digital_out = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(16)]
        offset += 64
        self.jnt_temperature = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.task_pc, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.task_repeat, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.task_run_id, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.task_run_num, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.task_run_time, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.task_state, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.default_speed, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.robot_state, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.information_chunk_1, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.reserved_1 = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.jnt_info = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.collision_detect_onoff, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.is_freedrive_mode, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.real_vs_simulation_mode, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.init_state_info, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.init_error, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.tfb_analog_in = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(2)]
        offset += 8
        self.tfb_digital_in = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(2)]
        offset += 8
        self.tfb_digital_out = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(2)]
        offset += 8
        self.tfb_voltage_out, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.op_stat_collision_occur, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.op_stat_sos_flag, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.op_stat_self_collision, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.op_stat_soft_estop_occur, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.op_stat_ems_flag, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.information_chunk_2, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.information_chunk_3, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.inbox_trap_flag = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(2)]
        offset += 8
        self.inbox_check_mode = [struct.unpack('i', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(2)]
        offset += 8
        self.eft_fx, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.eft_fy, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.eft_fz, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.eft_mx, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.eft_my, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.eft_mz, = struct.unpack('f', data[offset:offset+4])
        offset += 4
        self.information_chunk_4, = struct.unpack('i', data[offset:offset+4])
        offset += 4
        self.extend_io1_analog_in = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(4)]
        offset += 16
        self.extend_io1_analog_out = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(4)]
        offset += 16
        self.extend_io1_digital_info, = struct.unpack('I', data[offset:offset+4])
        offset += 4
        self.aa_joint_ref = [struct.unpack('f', data[offset+(i*4):offset+(i*4)+4])[0] for i in range(6)]
        offset += 24
        self.safety_board_stat_info, = struct.unpack('I', data[offset:offset+4])
        offset += 4




if __name__ == "__main__":
    data = b'$@\x02\x03\xaf\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x1ed\xb9\x00\x00\x00\x00\xe3\xa5\x9b\xbc\x89A@?\x04V\xce>9\xb4H\xbd9\xb4H=\xcd\xcc\xcc\xbc\x84\x07\x87\xbe\xa3\x8e\xc1\xc3F}\x89D\x00\x00\x00\x00\x00\x00\x00\x808c\x91\xbd\x84\x07\x87\xbe\xa3\x8e\xc1\xc3F}\x89D\x00\x00\x00\x00\x00\x00\x00\x808c\x91\xbd33#@33#@33#@33#@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$B\x00\x00\x1cB\x00\x00$B\x00\x008B\x00\x00<B\x00\x004B\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xcd\xccL?\x01\x00\x00\x00\x7f\xef\x92\xc4\x00\x00\x00\x004\xb3\xc1\xc3\xcd\x1c\x89D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x01\x07\x00\x00\x01\x07\x00\x00\x01\x07\x00\x00\x01\x07\x00\x00\x01\x07\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`KMT\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    a = RobotData()
    a.unpack(data)
    print(a.jnt_ref)

