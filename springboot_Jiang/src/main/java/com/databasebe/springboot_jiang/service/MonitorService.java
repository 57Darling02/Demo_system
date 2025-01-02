package com.databasebe.springboot_jiang.service;


import com.databasebe.springboot_jiang.mapper.MonitorDataMapper;
import com.databasebe.springboot_jiang.pojo.Monitor;
import com.databasebe.springboot_jiang.pojo.MonitorData;
import com.databasebe.springboot_jiang.pojo.ResponseMessage;
import com.databasebe.springboot_jiang.utils.JwtUtill;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

@Service
public class MonitorService implements IMonitorService {

    private static Long current_maxid = 0L;
    private final MonitorDataMapper monitorDataMapper;

    public MonitorService(MonitorDataMapper monitorDataMapper) {
        this.monitorDataMapper = monitorDataMapper;
    }

    @Override
    public ResponseMessage register(Integer monitor_id, String password) {
        Monitor u = monitorDataMapper.findByMonitorid(monitor_id);
        if(u != null){
            return ResponseMessage.error(500,"Monitor已存在");
        }else{
            monitorDataMapper.register(monitor_id,password);
            return ResponseMessage.success(null);
        }
    }

    @Override
    public ResponseMessage login(Integer monitor_id, String password) {
        Monitor loggingMonitor = monitorDataMapper.findByMonitorid(monitor_id);
        if (loggingMonitor == null){
            return ResponseMessage.error(401,"monitor不存在");
        }
        if(!loggingMonitor.getPassword().equals(password)){
            return ResponseMessage.error(401,"密码错误");
        }else {
            Map<String,Object> claims = new HashMap<>();
            claims.put("monitor_id",loggingMonitor.getMonitor_id());
            claims.put("last_login_time",LocalDateTime.now().toString());
            String token = JwtUtill.generateToken(claims);
            return ResponseMessage.success(token);
        }
    }

    @Override
    public ResponseMessage Stayalive(String token) {
        Map<String,Object> map = JwtUtill.parseToken(token);
        Integer monitor_id = (Integer) map.get("monitor_id");
        monitorDataMapper.aliveMonitor(monitor_id);
        return ResponseMessage.success(LocalDateTime.now());
    }

    @Override
    public ResponseMessage<String> upload_data(String token, LocalDateTime collect_time, Double humidity, String wind_direction, Double wind_speed, Double rainfall, Double air_temperature, String scene_type, Double air_pressure) {
        Map<String,Object> map = JwtUtill.parseToken(token);
        Integer monitor_id = (Integer) map.get("monitor_id");
        if(collect_time == null){
            collect_time = LocalDateTime.now();
        }
        monitorDataMapper.saveSensorData(monitor_id, collect_time,humidity, wind_direction, wind_speed, rainfall, air_temperature, scene_type, air_pressure);
        monitorDataMapper.aliveMonitor(monitor_id);
        return ResponseMessage.success("Data uploaded successfully");
    }

    @Override
    public ResponseMessage<Long> getMaxId() {
        Long maxId = monitorDataMapper.getMaxId();
        return ResponseMessage.success(maxId);
    }

    @Override
    public ResponseMessage<Boolean> ifUpdate() {
        Long maxId = monitorDataMapper.getMaxId();
        if(!Objects.equals(maxId, current_maxid)){
            current_maxid = maxId;
            return ResponseMessage.success(true);
        }
        return ResponseMessage.success(false);
    }

    @Override
    public ResponseMessage<List<Monitor>> getAllMonitor() {
        List<Monitor> result = monitorDataMapper.getAllMoncitor();
        return ResponseMessage.success(result);
    }

    @Override
    public ResponseMessage<List<MonitorData>> SearchMonitorData(Map<String, String> params) {
//        String sql = sqlUtil.buildQuery(params);
        List<MonitorData> result = monitorDataMapper.excuteQuery(params);
        return ResponseMessage.success(result);
    }

}
