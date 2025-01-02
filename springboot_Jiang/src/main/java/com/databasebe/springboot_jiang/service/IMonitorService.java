package com.databasebe.springboot_jiang.service;

import com.databasebe.springboot_jiang.pojo.ResponseMessage;

import java.time.LocalDateTime;
import java.util.Map;

public interface IMonitorService {
    ResponseMessage register(Integer monitor_id, String password);

    ResponseMessage login(Integer monitor_id, String password);

    ResponseMessage Stayalive(String token);


    ResponseMessage upload_data(String token, LocalDateTime collect_time, Double humidity, String wind_direction, Double wind_speed, Double rainfall, Double air_temperature, String scene_type, Double air_pressure);

    ResponseMessage getMaxId();

    ResponseMessage ifUpdate();

    ResponseMessage getAllMonitor();

    ResponseMessage SearchMonitorData(Map<String, String> params);
}
