import requests
import json
import uuid
from copy import deepcopy
import time
import re

def sort_locations_by_hierarchy(locations):
    """
    Sort locations by hierarchy level (parents first, then children)
    This ensures parent locations are created before child locations
    """
    if not locations:
        return locations
    
    # Sort by level (lower level = higher in hierarchy, should be created first)
    sorted_locations = sorted(locations, key=lambda x: x.get('level', 999))
    return sorted_locations

def find_parent_by_hierarchy(parent_type, parent_level, child_entity):
    """
    Find parent location by type and hierarchy level
    Generic approach that works for any location hierarchy
    """
    try:
        # Search for locations of the parent type at the parent level
        search_url = f"{base_url}/locations"
        response = requests.get(
            search_url,
            headers=headers,
            cookies=cookies,
            params={
                'size': 1000,
                'type': parent_type,
                'level': parent_level
            },
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            
            # Handle paginated response
            locations = []
            if isinstance(results, dict) and 'content' in results:
                locations = results['content']
            elif isinstance(results, list):
                locations = results
            
            # For now, return the first matching parent
            # In a more sophisticated system, you could use geographic proximity
            # or other criteria to find the most appropriate parent
            for location in locations:
                if (isinstance(location, dict) and 
                    location.get('type') == parent_type and 
                    location.get('level') == parent_level):
                    print(f"DEBUG: Found potential parent '{location.get('title')}' for '{child_entity.get('name')}'")
                    return location
            
            print(f"DEBUG: No parent of type '{parent_type}' at level {parent_level} found")
            return None
        else:
            print(f"WARNING: Parent search failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"ERROR: Exception in find_parent_by_hierarchy: {str(e)}")
        return None

def main(auth_token, org_type, config, user_name=None, org_name='test-suite', base_url='https://staging.avniproject.org'):
    """
    Comprehensive Avni Configuration Manager
    Handles: Validation → Creation → Verification → Progressive Updates
    Uses GET calls to verify actual state before attempting partial operations
    
    Args:
        auth_token (str): Avni authentication token
        org_type (str): Organization type ('Production', 'UAT', 'trial', etc.)
        config (dict): Configuration dictionary with entity definitions
        user_name (str, optional): User name for API calls
        org_name (str, optional): Organization name for cookies (default: 'test-suite')
        base_url (str, optional): Avni base URL (default: staging)
    """
    
    # API Endpoint mapping based on avni-webapp analysis
    API_ENDPOINTS = {
        'addressLevelType': '/addressLevelType',
        'locations': '/locations',
        'catchment': '/catchment',
        'subjectType': '/web/subjectType',
        'program': '/web/program',
        'encounterType': '/web/encounterType'
    }
    
    # Enhanced headers based on working curl request
    headers = {
        'auth-token': auth_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': base_url,
        'Referer': f'{base_url}/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'Sec-Ch-Ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=1, i'
    }
    
    # Add user-name header if provided
    if user_name:
        headers['user-name'] = user_name
    
    # Prepare cookies for session management (based on working curl)
    cookies = {
        'IMPLEMENTATION-NAME': org_name,
        'auth-token': auth_token,
        # Add PostHog analytics cookie if available (can be empty for basic functionality)
        'ph_phc_yLIQYtQjgTZJOl7ocZC9b26ruoWQCGYkLKUaqvOZN8s_posthog': '%7B%22distinct_id%22%3A%22test-user%22%7D'
    }
    
    # Debug: Print organization type for troubleshooting
    print(f"DEBUG: Organization type detected: '{org_type}'")
    
    # Check organization type - block Production/UAT to prevent accidental modifications
    # This complies with the assistant prompt requirement at line 122
    if org_type in ['Production', 'UAT']:
        return {
            'configResult': {
                'result': 'error',
                'message': 'We do not support automatic configurations for Production or UAT organisation types',
                'status': 'production_uat_blocked',
                'flow_action': 'block_creation'
            }
        }
    
    if not config or len(config) == 0:
        return {
            'configResult': {
                'result': 'error',
                'message': 'No configuration provided',
                'status': 'no_config',
                'flow_action': 'request_config'
            }
        }
    
    # Basic configuration validation
    if not config or not isinstance(config, dict):
        return {
            'configResult': {
                'result': 'error',
                'message': 'Invalid configuration format',
                'status': 'validation_failed',
                'flow_action': 'fix_validation_errors'
            }
        }
    
    def verify_entity_exists(entity_type, entity_name, entity_uuid=None, entity_id=None):
        """Use GET API to verify if entity exists by name, UUID, or ID"""
        try:
            # Map plural config keys to singular API endpoint keys
            entity_type_mapping = {
                'addressLevelTypes': 'addressLevelType',
                'locations': 'locations',
                'catchments': 'catchment',
                'subjectTypes': 'subjectType',
                'programs': 'program',
                'encounterTypes': 'encounterType'
            }
            
            api_entity_type = entity_type_mapping.get(entity_type, entity_type)
            endpoint = API_ENDPOINTS.get(api_entity_type)
            if not endpoint:
                return False, "Unknown entity type: " + str(entity_type)
            
            # Handle UUID-based lookup for locations
            if entity_uuid and api_entity_type == 'locations':
                # Direct UUID lookup for locations
                search_url = f"{base_url}/locations/web"
                response = requests.get(
                    search_url,
                    headers=headers,
                    cookies=cookies,
                    params={'uuid': entity_uuid},
                    timeout=10
                )
                
                if response.status_code == 200:
                    location_data = response.json()
                    print(f"DEBUG: Found location by UUID {entity_uuid}: {location_data.get('title', 'Unknown')}")
                    return True, location_data
                else:
                    print(f"DEBUG: Location with UUID {entity_uuid} not found")
                    return False, None
            
            # Special handling for different entity types
            if api_entity_type == 'addressLevelType':
                # AddressLevelType doesn't have a search endpoint, use the main GET endpoint
                # to fetch all address level types and search through them
                try:
                    search_url = base_url + endpoint
                    response = requests.get(
                        search_url,
                        headers=headers,
                        cookies=cookies,
                        params={'size': 1000},  # Get all address level types
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        # Handle paginated response structure
                        if isinstance(results, dict) and 'content' in results:
                            address_level_types = results['content']
                        elif isinstance(results, list):
                            address_level_types = results
                        else:
                            return False, "Unexpected response format from addressLevelType API"
                        
                        # Search for matching name (case-insensitive)
                        for alt in address_level_types:
                            if isinstance(alt, dict) and alt.get('name', '').lower() == entity_name.lower():
                                print(f"DEBUG: Found existing AddressLevelType '{entity_name}' with ID {alt.get('id')}")
                                return True, alt  # Return the actual AddressLevelType object
                        
                        print(f"DEBUG: AddressLevelType '{entity_name}' not found")
                        return False, None  # Not found in existing address level types
                    else:
                        return False, f"AddressLevelType verification failed: {response.status_code}"
                except Exception as e:
                    return False, f"AddressLevelType verification error: {str(e)}"
            else:
                # Different search patterns based on entity type
                if api_entity_type in ['subjectType', 'program', 'encounterType']:
                    # Web entities don't have search endpoints, use paginated get all
                    search_url = base_url + endpoint
                    response = requests.get(
                        search_url,
                        headers=headers,
                        cookies=cookies,
                        params={'size': 1000},  # Get all items to search through
                        timeout=10
                    )
                elif api_entity_type in ['locations', 'catchment']:
                    # These have dedicated search endpoints
                    if api_entity_type == 'locations':
                        search_url = base_url + endpoint + "/search/find"
                        # Use 'title' parameter for locations as per LocationController
                        response = requests.get(
                            search_url,
                            headers=headers,
                            cookies=cookies,
                            params={'title': entity_name},
                            timeout=10
                        )
                    else:  # catchment
                        search_url = base_url + endpoint + "/search/find"
                        # Use 'name' parameter for catchments
                        response = requests.get(
                            search_url,
                            headers=headers,
                            cookies=cookies,
                            params={'name': entity_name},
                            timeout=10
                        )
                else:
                    # Default fallback
                    search_url = base_url + endpoint + "/search"
                    response = requests.get(
                        search_url,
                        headers=headers,
                        cookies=cookies,
                        params={'name': entity_name},
                        timeout=10
                    )
            
            if response.status_code == 200:
                results = response.json()
                
                # Debug logging for locations
                if api_entity_type == 'locations':
                    print(f"DEBUG: Location search for '{entity_name}' returned: {results}")
                
                # Handle different response formats
                if api_entity_type in ['subjectType', 'program', 'encounterType']:
                    # Web entities return paginated results with _embedded structure
                    if isinstance(results, dict) and '_embedded' in results:
                        embedded_data = results['_embedded']
                        # Find the entity data in embedded response
                        for key in embedded_data:
                            if isinstance(embedded_data[key], list):
                                # Search through the list for matching name
                                for item in embedded_data[key]:
                                    if item.get('name') == entity_name:
                                        return True, None
                                return False, None
                    return False, None
                elif isinstance(results, dict) and api_entity_type == 'locations':
                    # Location search might return paginated response
                    if 'content' in results:
                        locations_list = results['content']
                        print(f"DEBUG: Location search returned paginated response with {len(locations_list)} items")
                        if len(locations_list) == 0:
                            return False, None
                        
                        # Check if any location matches exactly
                        for location in locations_list:
                            if isinstance(location, dict):
                                location_title = location.get('title', '')
                                print(f"DEBUG: Comparing '{entity_name}' with location '{location_title}'")
                                if location_title == entity_name:
                                    print(f"DEBUG: Found exact match for '{entity_name}'")
                                    return True, None
                        
                        print(f"DEBUG: No exact match found for '{entity_name}' in paginated results")
                        return False, None
                    else:
                        print(f"DEBUG: Location search returned dict but no 'content' key: {results}")
                        return False, None
                elif isinstance(results, list):
                    # For locations/catchments search results or direct arrays
                    if api_entity_type in ['locations', 'catchment']:
                        # These return search results directly
                        # Debug: Check what we actually got
                        found = len(results) > 0
                        if api_entity_type == 'locations':
                            # For locations, check if we have any results and if they match
                            if not found:
                                print(f"DEBUG: No locations found for '{entity_name}'")
                                return False, None
                            
                            # Check if any location in results matches our search term exactly
                            for location in results:
                                if isinstance(location, dict):
                                    location_title = location.get('title', '')
                                    print(f"DEBUG: Comparing '{entity_name}' with location '{location_title}'")
                                    if location_title == entity_name:
                                        print(f"DEBUG: Found exact match for '{entity_name}'")
                                        return True, None
                            
                            # If we have results but none match exactly, consider it not found
                            print(f"DEBUG: No exact match found for '{entity_name}' in {len(results)} results")
                            return False, None
                        return found, None
                    else:
                        # Direct array responses
                        return len(results) > 0, None
                else:
                    # Other response types
                    return bool(results), None
            else:
                return False, "Search failed: " + str(response.status_code)
        except Exception as e:
            return False, "Verification error: " + str(e)
    
    def find_locations_by_type_id(type_id):
        """Find locations by AddressLevelType ID using the findAsList endpoint"""
        try:
            search_url = f"{base_url}/locations/search/findAsList"
            response = requests.get(
                search_url,
                headers=headers,
                cookies=cookies,
                params={'typeId': type_id},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"DEBUG: Found {len(results) if isinstance(results, list) else 0} locations for typeId {type_id}")
                return results if isinstance(results, list) else []
            else:
                print(f"WARNING: Location search by typeId failed with status {response.status_code}")
                return []
                
        except Exception as e:
            print(f"ERROR: Exception in find_locations_by_type_id: {str(e)}")
            return []
    
    def should_be_parent(state_name, district_name):
        """Generic heuristic - for now, just return True to use first available parent"""
        # In a real system, this could use geographic data, naming patterns, or config hints
        # For this demo, we'll use the first available state as parent for districts
        return True
    
    def create_entity(entity_type, entity_data):
        """Create a single entity with proper validation"""
        try:
            # Map plural config keys to singular API endpoint keys
            entity_type_mapping = {
                'addressLevelTypes': 'addressLevelType',
                'locations': 'locations',
                'catchments': 'catchment',
                'subjectTypes': 'subjectType',
                'programs': 'program',
                'encounterTypes': 'encounterType'
            }
            
            api_entity_type = entity_type_mapping.get(entity_type, entity_type)
            endpoint = API_ENDPOINTS.get(api_entity_type)
            if not endpoint:
                return {
                    'status': 'error',
                    'message': "Unknown entity type: " + str(entity_type),
                    'status_code': 400
                }
            
            # Ensure UUID
            if 'uuid' not in entity_data or not entity_data['uuid']:
                entity_data['uuid'] = str(uuid.uuid4())
            
            # Transform data based on entity type
            if entity_type == 'locations':
                # Transform location data to match LocationContract structure
                location_data = {
                    'uuid': entity_data['uuid'],
                    'name': entity_data['name'],  # LocationContract uses 'name' field from ReferenceDataContract
                    'level': entity_data.get('level'),
                    'type': entity_data.get('type'),
                    'legacyId': entity_data.get('legacyId'),
                    'gpsCoordinates': entity_data.get('gpsCoordinates'),
                    'locationProperties': entity_data.get('locationProperties', {}),
                    'voided': entity_data.get('voided', False)
                }
                
                # CRITICAL: Look up existing AddressLevelType and use its ID, not UUID
                address_level_type_name = entity_data.get('type')
                if address_level_type_name:
                    alt_exists, alt_data = verify_entity_exists('addressLevelTypes', address_level_type_name)
                    if alt_exists and alt_data and isinstance(alt_data, dict):
                        # Use the actual ID from the existing AddressLevelType
                        location_data['typeId'] = alt_data.get('id')
                        print(f"DEBUG: Using existing AddressLevelType ID {alt_data.get('id')} for location '{entity_data['name']}'")
                    else:
                        print(f"WARNING: AddressLevelType '{address_level_type_name}' not found for location '{entity_data['name']}'")
                        # Still include the UUID as fallback
                        location_data['addressLevelTypeUUID'] = entity_data.get('addressLevelTypeUUID')
                
                # Handle parent relationship - use parentLocationUUID to find parentId
                if 'parentLocationUUID' in entity_data and entity_data['parentLocationUUID']:
                    parent_uuid = entity_data['parentLocationUUID']
                    
                    # Look up the parent location by UUID to get its database ID
                    parent_exists, parent_data = verify_entity_exists('locations', None, parent_uuid)
                    if parent_exists and parent_data and parent_data.get('id'):
                        location_data['parentId'] = parent_data.get('id')
                        print(f"DEBUG: Set parentId={parent_data.get('id')} for '{entity_data['name']}' using parentLocationUUID")
                    else:
                        print(f"WARNING: Parent location with UUID {parent_uuid} not found for '{entity_data['name']}'")
                elif entity_data.get('level', 0) > 1:
                    print(f"INFO: No parentLocationUUID provided for '{entity_data['name']}', cannot determine parent")
                # For top-level locations, don't include parent fields at all
                
                # CRITICAL FIX: Remove 'voided' field - it should be boolean, not string
                if 'voided' in location_data and isinstance(location_data['voided'], str):
                    location_data['voided'] = location_data['voided'].lower() == 'true'
                
                # Remove null values and empty objects
                location_data = {k: v for k, v in location_data.items() if v is not None and v != {}}
                data_to_send = [location_data]  # LocationController expects array
                
            elif entity_type == 'addressLevelTypes':
                # Transform address level type data
                alt_data = {
                    'uuid': entity_data['uuid'],
                    'name': entity_data['name'],
                    'level': entity_data.get('level'),
                    'parentId': entity_data.get('parentId'),
                    'voided': entity_data.get('voided', False)
                }
                # Remove null values
                alt_data = {k: v for k, v in alt_data.items() if v is not None}
                data_to_send = alt_data
                
            else:
                # For other entity types, use data as-is
                data_to_send = entity_data
            
            create_url = base_url + endpoint
            response = requests.post(
                create_url,
                headers=headers,
                cookies=cookies,
                data=json.dumps(data_to_send),
                timeout=30
            )
            
            success_msg = 'Created successfully'
            error_msg = "Creation failed: " + str(response.text)
            
            return {
                'status': 'success' if response.status_code < 400 else 'error',
                'status_code': response.status_code,
                'response': response.json() if response.status_code < 400 else response.text,
                'message': success_msg if response.status_code < 400 else error_msg
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': "Exception during creation: " + str(e),
                'status_code': 500
            }
    
    def process_entity_group(entity_type, entities, existing_check=True):
        """Process a group of entities with verification and progressive creation"""
        results = []
        
        for entity in entities:
            entity_name = entity.get('name', 'Unknown')
            
            # Step 1: Verify if entity already exists (if requested)
            if existing_check:
                exists, error = verify_entity_exists(entity_type, entity_name)
                if error:
                    results.append({
                        'name': entity_name,
                        'status': 'error',
                        'message': "Verification failed: " + str(error),
                        'status_code': 500,
                        'action': 'verification_failed'
                    })
                    continue
                
                if exists:
                    skip_msg = entity_type + " '" + entity_name + "' already exists"
                    results.append({
                        'name': entity_name,
                        'status': 'skipped',
                        'message': skip_msg,
                        'status_code': 200,
                        'action': 'already_exists'
                    })
                    continue
            
            # Step 2: Attempt creation
            creation_result = create_entity(entity_type, entity)
            creation_result['name'] = entity_name
            creation_result['action'] = 'created' if creation_result['status'] == 'success' else 'creation_failed'
            results.append(creation_result)
        
        return results
    
    try:
        # Initialize results structure
        configResult = {
            'addressLevelTypes': [],
            'locations': [],
            'catchments': [],
            'subjectTypes': [],
            'programs': [],
            'encounterTypes': [],
            'verification_enabled': True,
            'progressive_creation': True
        }
        
        # Entity processing order (respects dependencies)
        entity_order = [
            'addressLevelTypes',
            'locations',
            'catchments',
            'subjectTypes',
            'programs',
            'encounterTypes'
        ]
        
        # Process each entity type in dependency order
        for entity_type in entity_order:
            if entity_type in config and config[entity_type]:
                print(f"Processing {entity_type}...")
                
                entities = config[entity_type]
                
                # Special handling for locations - sort by hierarchy (parents first)
                if entity_type == 'locations':
                    entities = sort_locations_by_hierarchy(entities)
                    
                    # Create a mapping of location names to UUIDs for parent references
                    location_uuid_map = {}
                    for location in entities:
                        location_uuid_map[location.get('name', '')] = location.get('uuid', '')
                    
                    # Process locations - no hardcoded parent relationships
                    processed_locations = []
                    parent_locations_by_level = {}  # Track locations by level
                    
                    # First pass: group locations by level
                    for location in entities:
                        level = location.get('level')
                        if level not in parent_locations_by_level:
                            parent_locations_by_level[level] = []
                        parent_locations_by_level[level].append(location)
                    
                    # Second pass: process all locations
                    child_index_by_level = {}  # Track distribution index for each level
                    
                    for location in entities:
                        location_copy = location.copy()
                        current_level = location.get('level')
                        
                        # For child locations, find parent from previous level
                        if current_level and current_level > 1.0:
                            parent_level = current_level - 1.0
                            parent_locations = parent_locations_by_level.get(parent_level, [])
                            
                            if parent_locations:
                                # Initialize index for this level if not exists
                                if current_level not in child_index_by_level:
                                    child_index_by_level[current_level] = 0
                                
                                # Distribute children evenly among parents of previous level
                                parent_index = child_index_by_level[current_level] % len(parent_locations)
                                parent_location = parent_locations[parent_index]
                                parent_name = parent_location.get('name', '')
                                
                                if parent_name in location_uuid_map:
                                    location_copy['parentLocationUUID'] = location_uuid_map[parent_name]
                                    print(f"DEBUG: Assigned parent '{parent_name}' (level {parent_level}) to '{location.get('name')}' (level {current_level})")
                                
                                child_index_by_level[current_level] += 1
                            else:
                                print(f"WARNING: No parent locations found at level {parent_level} for '{location.get('name')}'")
                        
                        processed_locations.append(location_copy)
                    
                    configResult[entity_type] = process_entity_group(
                        entity_type, 
                        processed_locations,
                        existing_check=True
                    )
                else:
                    configResult[entity_type] = process_entity_group(
                        entity_type, 
                        config[entity_type],
                        existing_check=True
                    )
        
        # Analyze results
        total_entities = 0
        successful_entities = 0
        failed_entities = 0
        skipped_entities = 0
        
        for entity_type in entity_order:
            for entity in configResult.get(entity_type, []):
                total_entities += 1
                if entity.get('status') == 'success':
                    successful_entities += 1
                elif entity.get('status') == 'skipped':
                    skipped_entities += 1
                else:
                    failed_entities += 1
        
        # Determine flow action based on results
        if total_entities == 0:
            result = 'success'
            status = 'no_entities_to_process'
            flow_action = 'complete_success'
        elif successful_entities == total_entities:
            result = 'success'
            status = 'all_entities_created'
            flow_action = 'complete_success'
        elif successful_entities > 0 and failed_entities > 0:
            result = 'partial_success'
            status = 'partial_entities_created'
            flow_action = 'analyze_failures'
        elif skipped_entities == total_entities:
            result = 'success'
            status = 'all_entities_already_exist'
            flow_action = 'complete_success'
        elif failed_entities == total_entities:
            result = 'failure'
            status = 'all_entities_failed'
            flow_action = 'analyze_failures'
        else:
            result = 'partial_success'
            status = 'mixed_results'
            flow_action = 'analyze_failures'
        
        summary_msg = ("Processed " + str(total_entities) + " entities: " + 
                      str(successful_entities) + " created, " + 
                      str(skipped_entities) + " skipped, " + 
                      str(failed_entities) + " failed")
        
        return {
            'configResult': {
                'result': result,
                'status': status,
                'flow_action': flow_action,
                'message': summary_msg,
                'summary': {
                    'total': total_entities,
                    'successful': successful_entities,
                    'failed': failed_entities,
                    'skipped': skipped_entities
                },
                **configResult
            }
        }
        
    except Exception as error:
        error_msg = "Unexpected error: " + str(error)
        return {
            'configResult': {
                'result': 'error',
                'status': 'exception_occurred',
                'flow_action': 'handle_exception',
                'message': error_msg,
                'summary': {'total': 0, 'successful': 0, 'failed': 0, 'skipped': 0}
            }
        }
