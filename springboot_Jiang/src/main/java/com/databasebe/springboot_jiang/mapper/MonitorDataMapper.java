package com.databasebe.springboot_jiang.mapper;


import com.databasebe.springboot_jiang.pojo.Monitor;
import com.databasebe.springboot_jiang.pojo.MonitorData;
import com.databasebe.springboot_jiang.utils.sqlUtil;
import org.apache.ibatis.annotations.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Mapper
public interface MonitorDataMapper {
    @Insert("insert into monitor_data (monitor_id,upload_time,collect_time,wind_direction,wind_speed,humidity,rainfall,air_temperature,scene_type,air_pressure) " +
            "values (#{monitor_id},now(),#{collect_time},#{wind_direction},#{wind_speed},#{humidity},#{rainfall},#{air_temperature},#{scene_type},#{air_pressure})")
    void saveSensorData(Integer monitor_id, LocalDateTime collect_time, Double humidity, String wind_direction, Double wind_speed, Double rainfall, Double air_temperature, String scene_type, Double air_pressure);

    @Select("select * from monitor_info where monitor_id = #{monitorId}")
    Monitor findByMonitorid(Integer monitorId);


    @SelectProvider(type = sqlUtil.class,method = "buildQuery")
    List<MonitorData> excuteQuery(Map<String,String> params);

    @Update("update monitor_info set alive_time = now() where monitor_id = #{monitorId}")
    void aliveMonitor(Integer monitorId);

    @Select("SELECT MAX(Id) FROM monitor_data")
    Long getMaxId();
    @Insert("insert into monitor_info (monitor_id,password) values (#{monitor_id},#{password})")
    void register(Integer monitor_id, String password);
    @Select("select * from monitor_info")
    List<Monitor> getAllMoncitor();
}
