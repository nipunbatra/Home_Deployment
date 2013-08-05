//-----------------------------------------------------------------------------
//
//	Main.cpp
//
//	Minimal application to test OpenZWave.
//
//	Creates an OpenZWave::Driver and the waits.  In Debug builds
//	you should see verbose logging to the console, which will
//	indicate that communications with the Z-Wave network are working.
//
//	Copyright (c) 2010 Mal Lansell <mal@openzwave.com>
//
//
//	SOFTWARE NOTICE AND LICENSE
//
//	This file is part of OpenZWave.
//
//	OpenZWave is free software: you can redistribute it and/or modify
//	it under the terms of the GNU Lesser General Public License as published
//	by the Free Software Foundation, either version 3 of the License,
//	or (at your option) any later version.
//
//	OpenZWave is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU Lesser General Public License for more details.
//
//	You should have received a copy of the GNU Lesser General Public License
//	along with OpenZWave.  If not, see <http://www.gnu.org/licenses/>.
//
//-----------------------------------------------------------------------------

#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <iostream>
#include <ctime>
#include <time.h>
#include <fstream>
#include "Options.h"
#include "Manager.h"
#include "Driver.h"
#include "Node.h"
#include "Group.h"
#include "Notification.h"
#include "ValueStore.h"
#include "Value.h"
#include "ValueBool.h"
#include "Log.h"

/*
 *Command Classes for EZMotion-MultiSensor 
 */
#define COMMAND_CLASS_BASIC 0x20
#define COMMAND_CLASS_WAKE_UP 0x84
#define COMMAND_CLASS_BATTERY 0x80
#define COMMAND_CLASS_ALARM 0x71
#define COMMAND_CLASS_VERSION 0x86
#define COMMAND_CLASS_CONFIGURATION 0x70
#define COMMAND_CLASS_SENSOR_MULTILEVEL 0x31
#define COMMAND_CLASS_MULTI_INSTANCE 0x60

using namespace OpenZWave;
using namespace std;

int g_luminance[255]={0};
int g_temperature[255]={0};
static uint32 g_homeId = 0;
static bool   g_initFailed = false;
ofstream myCSV,myCSV1,myCSV2;
std::time_t t;
char b[11];
struct tm timeinfo;
char filename[30],filename1[30],filename2[30];
typedef struct
{
	uint32			m_homeId;
	uint8			m_nodeId;
	bool			m_polled;
	list<ValueID>	m_values;
}NodeInfo;

static list<NodeInfo*> g_nodes;
static pthread_mutex_t g_criticalSection;
static pthread_cond_t  initCond  = PTHREAD_COND_INITIALIZER;
static pthread_mutex_t initMutex = PTHREAD_MUTEX_INITIALIZER;

//-----------------------------------------------------------------------------
// <GetNodeInfo>
// Return the NodeInfo object associated with this notification
//-----------------------------------------------------------------------------
NodeInfo* GetNodeInfo
(
	Notification const* _notification
)
{
	uint32 const homeId = _notification->GetHomeId();
	uint8 const nodeId = _notification->GetNodeId();
	for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
	{
		NodeInfo* nodeInfo = *it;
		if( ( nodeInfo->m_homeId == homeId ) && ( nodeInfo->m_nodeId == nodeId ) )
		{
			return nodeInfo;
		}
	}

	return NULL;
}

//-----------------------------------------------------------------------------
// <configureSensorParameters>
// Configures several parameters for all the sensors.
//-----------------------------------------------------------------------------
void configureSensorParameters() 
{
    uint8 nodeId = 0;
	for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
	{
		NodeInfo* nodeInfo = *it;
        nodeId = nodeInfo->m_nodeId;

        // Initialize Configuration Parameters
        pthread_mutex_lock( &g_criticalSection );
        
        /* Request Sensitivity */
        Manager::Get()->SetConfigParam(g_homeId, nodeId, 1, 180); 
		Manager::Get()->RequestConfigParam(g_homeId, nodeId, 1);
		
        /* Request and Set the "On Time" Config Param to 20 with index 2 (See zwcfg*.xml) */
		Manager::Get()->SetConfigParam(g_homeId, nodeId, 2, 0); 
        Manager::Get()->RequestConfigParam(g_homeId, nodeId, 2); 

        /* Request "Stay Awake" Config Param */
        Manager::Get()->SetConfigParam(g_homeId, nodeId, 5, 255); 
        Manager::Get()->RequestConfigParam(g_homeId, nodeId, 5);
        
        /* Request and Set the "On Value" Config Param to 255 with index 6 (See zwcfg*.xml) */
        // Manager::Get()->SetConfigParam(g_homeId, Hsm100SensorId, 6, 255); 
        // Manager::Get()->RequestConfigParam(g_homeId, nodeId, 6); 

        pthread_mutex_unlock( &g_criticalSection );
    }
}

//-----------------------------------------------------------------------------
// <printConfigVariable>
// Prints the Configuration Variable
//-----------------------------------------------------------------------------
void printConfigVariable(uint8 index, uint8 byte_value) {
    static const char *parameter_names[] = {"Sensitivity", "On Time", "LED ON/OFF", 
        "Light Threshold", "Stay Awake", "On Value"};
    t = std::time(0); 
    myCSV.open(filename,fstream::app);
	myCSV<<ctime(&t)<<": "<<parameter_names[index-1]<<" was set to "<<byte_value<<"\n";
	myCSV.close();
    // printf("\"%s\" was set to %u\n", parameter_names[index-1], byte_value);
}

//-----------------------------------------------------------------------------
// <parseHsm100Sensor>
// Parses the HSM100 ValueChanged for luminance, temperature, motion, etc.
//-----------------------------------------------------------------------------
void parseHsm100Sensor(uint8 nodeId, ValueID value_id) {

    // Initialize Variables
    bool success = false;
    bool bool_value = false;
    uint8 byte_value = 0;
    float float_value = 0.0;
    int32 int_value = 0;
	// Perform action based on CommandClassID
    // For HSM-100, the following Classes need to be taken care of:
    // 1. COMMAND_CLASS_BASIC (0x20)
    // 2. COMMAND_CLASS_WAKE_UP (0x84)
    // 3. COMMAND_CLASS_BATTERY (0x80)
    // 4. COMMAND_CLASS_CONFIGURATION (0x70)
    // 5. COMMAND_CLASS_SENSOR_MULTILEVEL (0x31)
    // 6. COMMAND_CLASS_VERSION (0x86)
    
    // Print value parameters
    
       //printf("    ValueType: %d\n", (int) value_id.GetType());
       //printf("    ValueGenre: %d\n", (int) value_id.GetGenre());
       //printf("    Instance: %u\n", (uint8) value_id.GetInstance());
       //printf("    ID: %u\n", (uint64) value_id.GetId());
    

    // Get the Changed Value Based on the type
    switch((int) value_id.GetType()) {
        // See open-zwave/cpp/src/value_classes/ValueID.h for ValueType enum 
        case 0:
            // Boolean Type
            success = Manager::Get()->GetValueAsBool(value_id, &bool_value);
            break;
        case 1:
            // Byte Type
            success = Manager::Get()->GetValueAsByte(value_id, &byte_value);
            // printf("Successfully got Value? %s\n", (success)?"Yes":"No");
            break;
        case 2:
            // Float Type
            success = Manager::Get()->GetValueAsFloat(value_id, &float_value);
            break;
        case 3:
            // Int Type
            success = Manager::Get()->GetValueAsInt(value_id, &int_value);
            break;
        default:
            t = std::time(0); 
			myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Unrecognized Type: "<<(int) value_id.GetType()<<"\n";
			myCSV.close();
    
            // printf("Unrecognized Type: %d\n", (int) value_id.GetType());
            break;
    }
    if(!success) {
		t = std::time(0); 
		myCSV.open(filename,fstream::app);
		myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Unable to Get the Value \n";
		myCSV.close();
        // printf("Unable to Get the Value\n");
        return;
    }
    
    // Output based on the CommandClassId
    switch(value_id.GetCommandClassId()) {
        case COMMAND_CLASS_BASIC:
            t = std::time(0); 
			myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Got COMMAND_CLASS_BASIC!\n";
			myCSV.close();
        
            // printf("Got COMMAND_CLASS_BASIC!\n");
            // printf("It has been %u minutes-XXXXXX since the last Motion Detected.\n", byte_value);
            break;
        case COMMAND_CLASS_SENSOR_MULTILEVEL:
            t = std::time(0); 
			myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Got COMMAND_CLASS_SENSOR_MULTILEVEL!\n";
			myCSV.close();
        
            // printf("Got COMMAND_CLASS_SENSOR_MULTILEVEL!\n");

            // Report based on instance:
            // 1. General
            // 2. Luminance
            // 3. Temperature
            switch((uint8) value_id.GetInstance()) {
                case 1:
                    // General
                    t = std::time(0); 
                    myCSV.open(filename,fstream::app);
					myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Last Motion: "<<float_value<<"\n";
					myCSV.close();
                    break;
                case 2:
                    // Luminance
                    g_luminance[nodeId] = float_value;
                    t = std::time(0); 
                    myCSV.open(filename,fstream::app);
					myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Light: "<<g_luminance[nodeId]<<"\n";
					myCSV.close();
                    break;
                case 3:
                    // Temperature
                    g_temperature[nodeId]=float_value;
                    t = std::time(0); 
                    myCSV.open(filename,fstream::app);
					myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Temperature: "<<g_temperature[nodeId]<<"\n";
					myCSV.close();
                    break;

                default:
                    t = std::time(0); 
                    myCSV.open(filename,fstream::app);
					myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<"Unrecognized Instance\n";
					myCSV.close();
            
                    // printf("Unrecognized Instance\n");
                    break;
            }
            break;
        case COMMAND_CLASS_CONFIGURATION:
			t = std::time(0); 
            myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<"\nGot COMMAND_CLASS_CONFIGURATION!\n";
			myCSV.close();
			// printf("\nGot COMMAND_CLASS_CONFIGURATION!\n");
			printConfigVariable(value_id.GetIndex(), byte_value);
            break;
        case COMMAND_CLASS_WAKE_UP:
            t = std::time(0); 
            myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<"\nGot COMMAND_CLASS_WAKE_UP!\n"<<"Wake-up interval: "<<int_value<<" seconds\n";
			myCSV.close();
			
            // printf("\nGot COMMAND_CLASS_WAKE_UP!\n");
            // printf("Wake-up interval: %d seconds\n", int_value);
            // Manager::Get()->RefreshNodeInfo(g_homeId, nodeId);
            Manager::Get()->RequestNodeDynamic(g_homeId, nodeId);
            break;
        case COMMAND_CLASS_BATTERY:
			t = std::time(0); 
            myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<"\nGot COMMAND_CLASS_BATTERY!\n";
			// printf("\nGot COMMAND_CLASS_BATTERY!\n");
			Manager::Get()->GetValueAsByte(value_id, &byte_value);
            myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" BATTERY: "<<(int)byte_value<<"\n";
            // printf("Battery: %u\n", byte_value);
            myCSV.close();
            break;
        case COMMAND_CLASS_VERSION:
            t = std::time(0); 
            myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<"Got COMMAND_CLASS_VERSION!\n";
            // printf("Got COMMAND_CLASS_VERSION!\n");
            myCSV.close();
            break;
        default:
			t = std::time(0); 
            myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<"Got an Unknown COMMAND CLASS!\n";
            // printf("Got an Unknown COMMAND CLASS!\n");
            myCSV.close();
            break;
    }
    myCSV1.open(filename1,fstream::app);
	myCSV1<<t<<","<<(int)nodeId<<","<<g_luminance[nodeId]<<","<<g_temperature[nodeId]<<"\n";
	myCSV1.close();
                
}

//-----------------------------------------------------------------------------
// <OnNotification>
// Callback that is triggered when a value, group or node changes
//-----------------------------------------------------------------------------
void OnNotification
(
	Notification const* _notification,
	void* _context
)
{
	// Must do this inside a critical section to avoid conflicts with the main thread
	pthread_mutex_lock( &g_criticalSection );

	switch( _notification->GetType() )
	{
		case Notification::Type_ValueAdded:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				// Add the new value to our list
				nodeInfo->m_values.push_back( _notification->GetValueID() );
			}
			break;
		}

		case Notification::Type_ValueRemoved:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				// Remove the value from out list
				for( list<ValueID>::iterator it = nodeInfo->m_values.begin(); it != nodeInfo->m_values.end(); ++it )
				{
					if( (*it) == _notification->GetValueID() )
					{
						nodeInfo->m_values.erase( it );
						break;
					}
				}
			}
			break;
		}

		case Notification::Type_ValueChanged:
		{
			// One of the node values has changed
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
                // ValueID of value involved
                uint8 nodeId = nodeInfo->m_nodeId;
                ValueID value_id = _notification->GetValueID();
    			// printf("Received Value Change for Node %u\n", nodeId);
                // Perform different actions based on which node
                parseHsm100Sensor(nodeId, value_id);
			}
            break;
		}

		case Notification::Type_Group:
		{
			// One of the node's association groups has changed
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				nodeInfo = nodeInfo;		// placeholder for real action
			}
			break;
		}

		case Notification::Type_NodeAdded:
		{
			// Add the new node to our list
			NodeInfo* nodeInfo = new NodeInfo();
			nodeInfo->m_homeId = _notification->GetHomeId();
			nodeInfo->m_nodeId = _notification->GetNodeId();
			nodeInfo->m_polled = false;		
			g_nodes.push_back( nodeInfo );
			break;
		}

		case Notification::Type_NodeRemoved:
		{
			// Remove the node from our list
			uint32 const homeId = _notification->GetHomeId();
			uint8 const nodeId = _notification->GetNodeId();
			for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
			{
				NodeInfo* nodeInfo = *it;
				if( ( nodeInfo->m_homeId == homeId ) && ( nodeInfo->m_nodeId == nodeId ) )
				{
					g_nodes.erase( it );
					delete nodeInfo;
					break;
				}
			}
			break;
		}

		case Notification::Type_NodeEvent:
		{
			// We have received an event from the node, caused by a
            // basic_set or hail message.
            if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
            {
                
                // Initialize values
                ValueID value_id = _notification->GetValueID();
                uint8 nodeId = nodeInfo->m_nodeId;
				
				/*
				 * Event Based Motion Detection - Light and Temperature Values would also be Reported
				 */
				t = std::time(0); 
                myCSV.open(filename,fstream::app);
				myCSV<<ctime(&t)<<": NodeId-"<<(int)nodeId<<" Motion Detected\n";
				myCSV.close();
                
                myCSV2.open(filename2,fstream::app);
				myCSV2<<t<<","<<(int)nodeId<<"\n";
				myCSV2.close();
                // Manager::Get()->RefreshNodeInfo(g_homeId, nodeId);
                Manager::Get()->RequestNodeDynamic(g_homeId, nodeId);
                // printf("\n");
			}
			break;
		}

		case Notification::Type_PollingDisabled:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				nodeInfo->m_polled = false;
			}
			break;
		}

		case Notification::Type_PollingEnabled:
		{
			if( NodeInfo* nodeInfo = GetNodeInfo( _notification ) )
			{
				nodeInfo->m_polled = true;
			}
			break;
		}

		case Notification::Type_DriverReady:
		{
			g_homeId = _notification->GetHomeId();
			break;
		}

		case Notification::Type_DriverFailed:
		{
			g_initFailed = true;
			pthread_cond_broadcast(&initCond);
			break;
		}

		case Notification::Type_AwakeNodesQueried:
		case Notification::Type_AllNodesQueried:
		case Notification::Type_NodeQueriesComplete:
		case Notification::Type_AllNodesQueriedSomeDead:
		{
			pthread_cond_broadcast(&initCond);
			break;
		}
		case Notification::Type_Notification:
		{
			int node = _notification->GetNodeId();
			int code = _notification->GetNotification();
			/*
			 * Saving Notification Code by Every Node to Timestamp based Log File
			 */
			t = std::time(0); 
            myCSV.open(filename,fstream::app);
			myCSV<<ctime(&t)<<": NodeId-"<<(int)node<<" Notification Code: "<<code<<"\n";
			myCSV.close();
			
			break;
		}
		
		case Notification::Type_DriverReset:
		case Notification::Type_NodeNaming:
		case Notification::Type_NodeProtocolInfo:
		default:
		{
		}
	}

	pthread_mutex_unlock( &g_criticalSection );
}

//-----------------------------------------------------------------------------
// <main>
// Create the driver and then wait
//-----------------------------------------------------------------------------
int main( int argc, char* argv[] )
{
	pthread_mutexattr_t mutexattr;

	pthread_mutexattr_init ( &mutexattr );
	pthread_mutexattr_settype( &mutexattr, PTHREAD_MUTEX_RECURSIVE );
	pthread_mutex_init( &g_criticalSection, &mutexattr );
	pthread_mutexattr_destroy( &mutexattr );
	
	pthread_mutex_lock( &initMutex );
	/*Every Time Program Starts a Log File is generated Based on Timestamp*/
	t = std::time(0);
	// timeinfo = *localtime(&t);
	// strftime(b, sizeof(b), "%m%d%H%M%y", &timeinfo);
	printf("%s",ctime(&t));
	sprintf(filename,"ZWaveLog/Log_%d.csv",t);
	// printf("%s",ctime(&t));
	sprintf(filename1,"LT_Data/LT_Data_%d.csv",t);
	// printf("%s",ctime(&t));
	sprintf(filename2,"M_Data/M_Data_%d.csv",t);
	
	
	// Create the OpenZWave Manager.
	// The first argument is the path to the config files (where the manufacturer_specific.xml file is located
	// The second argument is the path for saved Z-Wave network state and the log file.  If you leave it NULL 
	// the log file will appear in the program's working directory.
	
	Options::Create( "../source_library/config/", "", "" );
	Options::Get()->AddOptionInt( "SaveLogLevel", LogLevel_Detail );
	Options::Get()->AddOptionInt( "QueueLogLevel", LogLevel_Debug );
	Options::Get()->AddOptionInt( "DumpTrigger", LogLevel_Error );
	Options::Get()->AddOptionInt( "PollInterval", 60000 );
	Options::Get()->AddOptionBool( "IntervalBetweenPolls", false );
	Options::Get()->AddOptionBool("ValidateValueChanges", false);
	
	// Turn off Console Logging
    Options::Get()->AddOptionBool("ConsoleOutput", false);
    Options::Get()->AddOptionBool("Logging", true);
	
	Options::Get()->Lock();

	Manager::Create();

	// Add a callback handler to the manager.  The second argument is a context that
	// is passed to the OnNotification method.  If the OnNotification is a method of
	// a class, the context would usually be a pointer to that class object, to
	// avoid the need for the notification handler to be a static.
	Manager::Get()->AddWatcher( OnNotification, NULL );

	// Add a Z-Wave Driver
	// Modify this line to set the correct serial port for your PC interface.

	string port = "/dev/ttyUSB0";
	if ( argc > 1 )
	{
		port = argv[1];
	}
	if( strcasecmp( port.c_str(), "usb" ) == 0 )
	{
		Manager::Get()->AddDriver( "HID Controller", Driver::ControllerInterface_Hid );
	}
	else
	{
		Manager::Get()->AddDriver( port );
	}

	// Now we just wait for either the AwakeNodesQueried or AllNodesQueried notification,
	// then write out the config file.
	// In a normal app, we would be handling notifications and building a UI for the user.
	pthread_cond_wait( &initCond, &initMutex );

	// Since the configuration file contains command class information that is only 
	// known after the nodes on the network are queried, wait until all of the nodes 
	// on the network have been queried (at least the "listening" ones) before
	// writing the configuration file.  (Maybe write again after sleeping nodes have
	// been queried as well.)
	if( !g_initFailed )
	{
		/*Write to XML*/
		Manager::Get()->WriteConfig( g_homeId );
		t = std::time(0); 
        myCSV.open(filename,fstream::app);
		myCSV<<ctime(&t)<<": Configuration Written\n ";
		myCSV.close();
		// printf("Configuration Written\n");
		
		// The section below demonstrates setting up polling for a variable.  In this simple
		// example, it has been hardwired to poll COMMAND_CLASS_BASIC on the each node that 
		// supports this setting.
		pthread_mutex_lock( &g_criticalSection );
		uint8 ccId = 0;
        uint8 nodeId = 0;
		for( list<NodeInfo*>::iterator it = g_nodes.begin(); it != g_nodes.end(); ++it )
		{
			NodeInfo* nodeInfo = *it;

			// skip the controller (most likely node 1)
			if( nodeInfo->m_nodeId == 1) continue;
			else
			{
				for( list<ValueID>::iterator it2 = nodeInfo->m_values.begin(); it2 != nodeInfo->m_values.end(); ++it2 )
				{	
					ValueID v = *it2;
					ccId = v.GetCommandClassId();
					if(ccId == COMMAND_CLASS_WAKE_UP) {
						// Set the Wake-up interval
						bool success = Manager::Get()->SetValue(v, 90000);
						// printf("Set Wake-up Interval Successfully: %s\n", (success)?"Yes":"No");
					}
					if(ccId == COMMAND_CLASS_SENSOR_MULTILEVEL) {
						Manager::Get()->EnablePoll(v,6);
					}
				}
			}
		}
		pthread_mutex_unlock( &g_criticalSection );
		/*
		 * Configure Sensor Parameters
		 */ 
		configureSensorParameters();
		// printf("Parameters Configured\n");
		// If we want to access our NodeInfo list, that has been built from all the
		// notification callbacks we received from the library, we have to do so
		// from inside a Critical Section.  This is because the callbacks occur on other 
		// threads, and we cannot risk the list being changed while we are using it.  
		// We must hold the critical section for as short a time as possible, to avoid
		// stalling the OpenZWave drivers.
		// At this point, the program just waits for 3 minutes (to demonstrate polling),
		// then exits
		// while(1)
		for( int i = 0; i < 60*60; i++ )
		{
			// pthread_mutex_lock( &g_criticalSection );
			// but NodeInfo list and similar data should be inside critical section
			// pthread_mutex_unlock( &g_criticalSection );
			sleep(1);
		}

		Driver::DriverData data;
		Manager::Get()->GetDriverStatistics( g_homeId, &data );
		t = std::time(0); 
        myCSV.open(filename,fstream::app);
		myCSV<<ctime(&t)<<": SOF: "<<data.m_SOFCnt<<" ACK Waiting: "<<data.m_ACKWaiting<<" Read Aborts: "<<data.m_readAborts<<" Bad Checksums: "<<data.m_badChecksum<<"\n";
		myCSV<<ctime(&t)<<": Reads: "<<data.m_readCnt<<" Writes: "<<data.m_writeCnt<<" CAN: "<<data.m_CANCnt<<" NAK: "<<data.m_NAKCnt<<" ACK: "<<data.m_ACKCnt<<" Out of Frame: "<<data.m_OOFCnt<<"\n";
		myCSV<<ctime(&t)<<": Dropped: "<<data.m_dropped<<" Retries: "<<data.m_retries<<"\n";
		myCSV.close();
		// printf("SOF: %d ACK Waiting: %d Read Aborts: %d Bad Checksums: %d\n", data.m_SOFCnt, data.m_ACKWaiting, data.m_readAborts, data.m_badChecksum);
		// printf("Reads: %d Writes: %d CAN: %d NAK: %d ACK: %d Out of Frame: %d\n", data.m_readCnt, data.m_writeCnt, data.m_CANCnt, data.m_NAKCnt, data.m_ACKCnt, data.m_OOFCnt);
		// printf("Dropped: %d Retries: %d\n", data.m_dropped, data.m_retries);
	}
	// program exit (clean up)
	if( strcasecmp( port.c_str(), "usb" ) == 0 )
	{
		Manager::Get()->RemoveDriver( "HID Controller" );
	}
	else
	{
		Manager::Get()->RemoveDriver( port );
	}
	Manager::Get()->RemoveWatcher( OnNotification, NULL );
	Manager::Destroy();
	Options::Destroy();
	pthread_mutex_destroy( &g_criticalSection );
	return 0;
}
