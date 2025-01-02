package com.databasebe.springboot_jiang.controller;
import com.databasebe.springboot_jiang.pojo.MonitorData;
import com.databasebe.springboot_jiang.pojo.ResponseMessage;
import com.databasebe.springboot_jiang.service.IMonitorService;
import jakarta.validation.constraints.Pattern;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/monitor")
public class MonitorController {
    private final IMonitorService monitorService;

    public MonitorController(IMonitorService monitorService) {
        this.monitorService = monitorService;
    }

    @GetMapping("/ifUpdate")
    public ResponseMessage ifUpdate(){
        return monitorService.ifUpdate();
    }

    @GetMapping("/getMaxDataId")
    public ResponseMessage getMaxDataId(){
        return monitorService.getMaxId();
    }

    @GetMapping("/monitorList")
    public ResponseMessage monitorList(){
        return monitorService.getAllMonitor();
    }

    @GetMapping("/searchData")
    public ResponseMessage<List<MonitorData>> searchData(@RequestBody Map<String,String> params){
        return monitorService.SearchMonitorData(params);
    }

    @GetMapping("/getAllData")
    public ResponseMessage getAllData(){
        return monitorService.SearchMonitorData(new HashMap<>());
    }

    @PostMapping("/register")
    public ResponseMessage register(@Pattern(regexp = "^\\d{1,10}$")String monitor_id, @Pattern(regexp = "^\\S{5,16}$")String password){
        Integer Monitor_id = Integer.parseInt(monitor_id);
        return monitorService.register(Monitor_id,password);
    }

    @PostMapping("/login")
    public ResponseMessage<String> login(Integer monitor_id, @Pattern(regexp = "^\\S{5,16}$")String password){
        return monitorService.login(monitor_id,password);
    }


    @PostMapping("/uploadData")
    public ResponseMessage uploadData(
            @RequestHeader(name = "Authorization") String token,
            @RequestParam(required = false) @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss") LocalDateTime collect_time,
            @RequestParam(required = false) Double humidity,
            @RequestParam(required = false) String wind_direction,
            @RequestParam(required = false) Double wind_speed,
            @RequestParam(required = false) Double rainfall,
            @RequestParam(required = false) Double air_temperature,
            @RequestParam(required = false) String scene_type,
            @RequestParam(required = false) Double air_pressure
            ) {

        return monitorService.upload_data(token, collect_time,humidity, wind_direction, wind_speed, rainfall, air_temperature, scene_type, air_pressure);
    }
    @PostMapping("/alive")
    public ResponseMessage Stayalive(@RequestHeader(name = "Authorization") String token){
        return monitorService.Stayalive(token);
    }

}
