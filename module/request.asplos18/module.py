#
# Collective Knowledge: CK-powered AI/SW/HW co-design for ReQuEST tournaments
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, cTuning foundation/dividiti
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
line='================================================================'

experiment_tags='request-asplos18'
experiment_repos=['local','ck-request','ck-request-asplos18-results']

form_name='request_web_form'
onchange='document.'+form_name+'.submit();'

hextra='<center>\n'
hextra+='<p>\n'
hextra+=' Results from <a href="http://cknowledge.org/request-cfp-asplos2018.html">open ReQuEST @ ASPLOS\'18 tournament</a>\n'
hextra+='</center>\n'
hextra+='<p>\n'

selector=[
          {'name':'Species', 'key':'species'},
          {'name':'Type', 'key':'prog_type'},
          {'name':'Test', 'key':'prog_uoa'},
          {'name':'Dataset', 'key':'dataset_uoa'},
          {'name':'Platform', 'key':'plat_name', 'new_line':'yes'},
          {'name':'Time stamp', 'key':'timestamp'}
         ]

selector2=[
           {'name':'OpenCL driver', 'key':'##features#gpgpu@0#gpgpu_misc#opencl c version#min', 'skip_empty':'yes', 
                              'extra_key':'##features#gpgpu@0#gpgpu_misc#opencl_c_version#min'},
           {'name':'Dataset file', 'key':'##choices#env#CK_DATASET_FILENAME#min', 'new_line':'yes'},
           {'name':'Batch size', 'key':"##choices#env#CK_IN_SHAPE_N#min", 'type':'int'},
          ]

selector3=[
           {'name':'Plot time in', 'key':'plot_time_in'}
          ]

wchoices3={
            'plot_time_in':[
              {'name':'sec', 'value':'sec'},
              {'name':'ms', 'value':'ms'}
            ]}

k_hi_uid='highlight_behavior_uid'
k_hi_user='highlight_by_user'
k_view_all='all'

hidden_keys=[k_hi_uid, k_hi_user, k_view_all]

view_cache=[
  "##choices#env#CK_ABS_DIFF_THRESHOLD#min",
  "##choices#env#CK_DATASET_FILENAME#min",
  "##choices#env#CK_IN_SHAPE_C#min",
  "##choices#env#CK_IN_SHAPE_H#min",
  "##choices#env#CK_IN_SHAPE_N#min",
  "##choices#env#CK_IN_SHAPE_W#min",
  "##choices#env#CK_POOL_KERNEL#min",
  "##choices#env#CK_POOL_PAD_SCHEME#min",
  "##choices#env#CK_POOL_STRIDE#min",
  "##choices#env#CK_SEED#min",
  "##pipeline_state#fail_bool#min",
  "##pipeline_state#fail_reason#min",
  "##characteristics#compile#compilation_success_bool#min",
  "##characteristics#run#run_success_bool#min",
  "##characteristics#run#output_check_failed_bool#min",
  "##characteristics#run#execution_time#min",
  "##characteristics#run#execution_time#max",
  "##characteristics#run#run_time_state#time_test#min",
  "##characteristics#run#run_time_state#time_test#max",
  "##characteristics#run#run_time_state#time_setup#min",
  "##characteristics#run#run_time_state#time_setup#max",
  "##features#gpgpu@0#gpgpu_misc#opencl c version#min"
]

table_view=[
  {"key":"##meta#prog_uoa", "name":"Test", "skip_if_key_in_input":"prog_uoa"},
  {"key":"##meta#dataset_uoa", "name":"Dataset", "skip_if_key_in_input":"dataset_uoa"},
  {"key":"##meta#plat_name", "name":"Platform", "skip_if_key_in_input":"plat_name"},
  {"key":"##meta#timestamp", "name":"Time stamp", "skip_if_key_in_input":"timestamp"},
  {"key":"##meta#versions", "name":"Versions", "json_and_pre":"yes", "align":"left"},
  {"key":"##choices#env#", "name":"Environment", "starts_with":"yes", "align":"left"},
  {"key":"##characteristics#run#execution_time#min", "name":"Total time (sec. min/max)", "check_extra_key":"max", "format":"%.2e"},
  {"key":"##characteristics#run#run_time_state#time_setup#min", "name":"Setup time (sec. min/max)", "check_extra_key":"max", "format":"%.2e"},
  {"key":"##characteristics#run#run_time_state#time_test#min", "name":"Test time (sec. min/max)", "check_extra_key":"max", "format":"%.2e"},
  {"key":"##meta#user", "name":"User"},
  {"key":"##extra#html_replay_button", "name":"Replay"}
]

prune_first_level=100
prune_second_level=400

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# show results

def show(i):
    """
    Input:  {
               (crowd_module_uoa)       - if rendered from experiment crowdsourcing
               (crowd_key)              - add extra name to Web keys to avoid overlapping with original crowdsourcing HTML
               (crowd_on_change)        - reuse onchange doc from original crowdsourcing HTML

               (highlight_behavior_uid) - highlight specific result (behavior)!
               (highlight_by_user)      - highlight all results from a given user

               (refresh_cache)          - if 'yes', refresh view cache
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import copy
    import time

    # Preparing various parameters to render HTML dashboard
    st=''

    view_all=i.get(k_view_all,'')

    cmuoa=i.get('crowd_module_uoa','')
    ckey=i.get('crowd_key','')

    if 'reset_'+form_name in i: reset=True
    else: reset=False

    if 'all_choices_'+form_name in i: all_choices=True
    else: all_choices=False

    debug=(i.get('debug','')=='yes')
#    debug=True

    conc=i.get('crowd_on_change','')
    if conc=='':
        conc=onchange

    hi_uid=i.get(k_hi_uid,'')
    hi_user=i.get(k_hi_user,'')

    refresh_cache=i.get('refresh_cache','')

    bd='<div style="background-color:#bfffbf;margin:5px;">'

#    h='<hr>\n'
    h='<center>\n'
    h+='\n\n<script language="JavaScript">function copyToClipboard (text) {window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);}</script>\n\n' 

    h+=hextra

#    h+='<hr>\n'
#    h+='<br>\n'

    # Check host URL prefix and default module/action *********************************************
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe',
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']
    template=rx['template']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # Check and add hidden keys ***************************************************
    h+='\n\n'

    for k in hidden_keys:
        if i.get(k,'')!='':
           h+='<input type="hidden" name="'+k+'" value="'+i[k]+'">\n'

    h+='\n\n'

    # Prepare first level of selection with pruning ***********************************************
    r=ck.access({'action':'prepare_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'original_input':i,
                 'tags':experiment_tags,
                 'search_repos':experiment_repos,
                 'debug': debug,
                 'selector':selector,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'url1':url1,
                 'form_name':form_name,
                 'background_div':bd,
                 'skip_html_selector':'yes'})
    if r['return']>0: return r

    olst=r['lst'] # original list (if all_choices)
    plst=r['pruned_lst']

    # Sort list ***********************************************************************************
    dt=time.time()
    splst=sorted(plst, key=lambda x: (
        x.get('meta',{}).get('meta',{}).get('prog_uoa',''), 
        x.get('meta',{}).get('meta',{}).get('dataset_uoa',''), 
        x.get('meta',{}).get('meta',{}).get('plat_name',''), 
        x.get('meta',{}).get('meta',{}).get('timestamp','')
        ))

    if debug: h+='\n<p>Debug time (sorting table): '+str(time.time()-dt)+' sec.<p>\n'

    # Prune list **********************************************************************************
    len_splst=len(splst)
    if len_splst>prune_first_level:
       splst=splst[:prune_first_level]

       h+='\n<i>Showing '+str(prune_first_level)+' of '+str(len_splst)+' entries ...</i><br>\n'

    # Prepare and cache results for the table
    r=ck.access({'action':'get_and_cache_results',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'lst':splst,
                 'cache_uid':work['self_module_uid'],
                 'refresh_cache':refresh_cache,
                 'view_cache':view_cache,
                 'table_view':table_view})
    if r['return']>0: return 
    table=r['table']

    # Prepare second level of selection with pruning ***********************************************
    r=ck.access({'action':'prepare_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'original_input':i,
                 'tags':experiment_tags,
                 'search_repos':experiment_repos,
                 'lst':table,
                 'skip_meta_key':'yes',
                 'debug': debug,
                 'selector':selector2,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'url1':url1,
                 'form_name':form_name,
                 'skip_form_init':'yes',
                 'background_div':bd})
    if r['return']>0: return r

    h2=r['html']
    table=r['pruned_lst']

    choices2=r['choices']
    wchoices2=r['wchoices']

    # Extra fields (customized for this module) *****************************************************************************
    for row in table:
        duoa=row.get('##data_uid','')
        dpoint=row.get('##point_uid','')

        x=''
        if duoa!='' and dpoint!='':
           x='ck replay experiment:'+duoa+' --point='+str(dpoint)
           y=ck.cfg.get('add_extra_to_replay','')
           if y!='':x+=' '+y

        row['##extra#html_replay_button']='<input type="button" class="ck_small_button" onClick="copyToClipboard(\''+x+'\');" value="Copy to clipboard">\n'

    # Prune first list based on second selection*****************************************************************************
    if all_choices:
       nsplst=olst
    elif reset:
       nsplst=splst
    else:
       all_uid=[]
       for row in table:
           duid=row.get('##data_uid','')
           if duid!='' and duid not in all_uid:
              all_uid.append(duid)

       nsplst=[]
       for q in splst:
           if q['data_uid'] in all_uid:
              nsplst.append(q)

    # Check if too many *****************************************************************************************************
    ltable=len(table)
    min_view=False

    hx=''
    if ltable==0:
        h+='<b>No results found!</b>'
        return {'return':0, 'html':h, 'style':st}

    elif ltable>prune_second_level and view_all!='yes':
       table=table[:prune_second_level]

       hx='\n<i>Showing '+str(prune_second_level)+' of '+str(ltable)+' entries ...</i><br>\n'

    # Get unique values and create html selector 1 (after selector 2)
    r=ck.access({'action':'get_unique_keys_from_list',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'lst':nsplst,
                 'selector':selector,
                 'crowd_key':ckey,
                 'original_input':i})
    if r['return']>0: return 

    choices1=r['choices']
    wchoices1=r['wchoices']

    # Prepare selector 1  (based on choices from selector 2)
    r=ck.access({'action':'prepare_html_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'start_form':'yes',
                 'url1':url1,
                 'form_name':form_name,
                 'background_div':bd,
                 'selector':selector,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'wchoices':wchoices1,
                 'original_input':i})
    if r['return']>0: return r
    h1=r['html']

    h+=h1+'\n'+h2

    ltable=len(table)
    min_view=False

    if ltable==0:
        h+='<b>No results found!</b>'
        return {'return':0, 'html':h, 'style':st}

    elif ltable>prune_second_level and view_all!='yes':
       table=table[:prune_second_level]

       h+='\n<i>Showing '+str(prune_second_level)+' of '+str(ltable)+' entries ...</i><br>\n'

    # Prepare selector 3 (without pruning - about tables and graphs)
    if len(selector3)>0:
       r=ck.access({'action':'prepare_html_selector',
                    'module_uoa':cfg['module_deps']['experiment'],
                    'start_form':'no',
                    'url1':url1,
                    'form_name':form_name,
                    'background_div':bd,
                    'selector':selector3,
                    'crowd_key':ckey,
                    'crowd_on_change':conc,
                    'wchoices':wchoices3,
                    'original_input':i,
                    'add_reset':'yes'})
       if r['return']>0: return r
       h+='\n'+r['html']+'\n'

    h+='\n'+hx+'\n'

    # Prepare graph *********************************************************************************************************
    bgraph={'0':[]}
    igraph={'0':[]}

    stable=sorted(table, key=lambda row: (
        ck.safe_float(row.get('##characteristics#run#execution_time#min',None),0.0)
        ))

    xtscale=i.get('plot_time_in','')
    tscale=1.0
    if xtscale=='ms':
       tscale=1000.0

    ix=0
    for row in stable:
        ix+=1
        six=str(ix)

        x=row.get('##characteristics#run#execution_time#min',None)
        if type(x)!=float: 
           tmin=0.0
        else:
           tmin=x*tscale

        x=row.get('##characteristics#run#execution_time#max',None)
        if type(x)!=float: 
           tmax=tmin
        else:
           tmax=x*tscale

        tdelta=0.0
        if tmin!=0.0 and tmax!=0.0:
           tdelta=tmax-tmin

        bgraph['0'].append([ix,tmin, tmin+tdelta])

        raw_data_url=url0#+'wcid='+x+':'+duid

#        igraph['0'].append({'size':sizem, 'color':xcol, 'features':row, 'url':'', 'url_ext':raw_data_url})
        igraph['0'].append({'size':4, 'features':row, 'anchor':'id'+six}) #, 'url':'', 'url_ext':''})


    if len(bgraph['0'])>0:
       dt=time.time()
       ii={'action':'plot',
           'module_uoa':cfg['module_deps']['graph'],

           "table":bgraph,
           "table_info":igraph,

           "xmin":0,
           "ymin":0,

           "ignore_point_if_none":"yes",

           "plot_type":"d3_2d_scatter",

           "display_y_error_bar2":"yes",

           "title":"Powered by Collective Knowledge",

           "x_ticks_period":10,

           "axis_x_desc":"Experiment",
           "axis_y_desc":"Total kernel execution time ("+xtscale+")",

           "plot_grid":"yes",

           "d3_div":"ck_interactive",

           "image_width":"900",
           "image_height":"400",

           "wfe_url":url0}

       r=ck.access(ii)
       if r['return']==0:
          x=r.get('html','')
          if x!='':
             st+=r.get('style','')

             h+='<center>\n'
             h+='<div id="ck_box_with_shadow" style="width:940px;">\n'
             h+=' <div id="ck_interactive" style="text-align:center;font-size:11px;">\n'
             h+=x+'\n'
             h+=' </div>\n'
             h+='</div>\n'
             h+='</center>\n'
             h+='<br>\n'

    # In the future, we may want to use Django + numpy here
    # Prepare table header ******************************************************************
    bgc='dfffdf'
    bg=' style="background-color:#'+bgc+';"'
    bg1=' style="background-color:#bfffbf;"'
    bg2=' style="background-color:#afffaf;"'

    h+='<small><table border="1" cellpadding="7" cellspacing="0">\n'

    ha='align="$#align#$" valign="top"'

    # Prepare table header *****************************************************************
    h+='  <tr style="background-color:#dddddd">\n'

    h+='   <td '+ha.replace('$#align#$','center')+'><b>#</b></td>\n'

    for tv in table_view:
        k=tv['key']

        align=tv.get('align','')
        if align=='': align='center'

        skip=False

        kk=tv.get('skip_if_key_in_input','')
        if kk!='' and i.get(kk,'')!='':
           skip=True

        if not skip:
           n=tv.get('name','')
           if n=='': n=k

           h+='   <td '+ha.replace('$#align#$',align)+'><b>'+n+'</b></td>\n'

    h+='  </tr>\n'

    # Draw table ***************************************************************************
    dt=time.time()
    ix=0
    for q in table:
        ix+=1
        six=str(ix)

        # Check colors
        bgx=bg
        bgx1=bg1
        bgx2=bg2
        if (hi_uid!='' and duid==hi_uid) or (hi_user!='' and hi_user==user):
           bgx=' style="background-color:#ffcf7f"'
           bgx1=' style="background-color:#ffbf5f"'
           bgx2=' style="background-color:#ffaf2f"'

        # Starting raw ***************************************
        h+='  <tr'+bgx+'>\n'

        h+='   <td '+ha.replace('$#align#$','center')+'><a name="id'+six+'" id="id'+six+'">'+six+'</a></td>\n'

        for tv in table_view:
            k=tv['key']

            align=tv.get('align','')
            if align=='': align='center'

            skip=False

            kk=tv.get('skip_if_key_in_input','')
            if kk!='' and i.get(kk,'')!='':
               skip=True

            if not skip:
               v=q.get(k,'')

               format=tv.get('format','')
               if format!='' and v!='' and v!=None:
                  v=format % float(v)

               if tv.get('json_and_pre','')=='yes' and v!='' and type(v)==dict:
                  v1=''
                  for kx in v:
                      v1+=kx+'='+str(v[kx])+'<br>'
                  v=v1

#                  import json
#                  v='<pre>'+json.dumps(v, indent=2, sort_keys=True)+'</pre>'

               if tv.get('starts_with','')=='yes':
                  v=''
                  for kx in sorted(q):
                      if kx!=k and kx.startswith(k):
                         v+=kx[len(k):-4]+'='+str(q.get(kx,''))+'<br>'

               v=str(v)

               cek=tv.get('check_extra_key','')
               if cek!='':
                  j=k.rfind('#')
                  if j>0:
                     k1=k[:j+1]+cek

                     v1=q.get(k1,'')

                     if format!='' and v1!='' and v1!=None:
                        v1=format % float(v1)

                     v1=str(v1)

                     if v1!='':
                        v+=' .. '+v1

               h+='   <td '+ha.replace('$#align#$',align)+'>'+v+'</td>\n'

        h+='  <tr>\n'

    h+='</table></small>\n'
    h+='</center>\n'

    if debug: h+='\n<p>Debug time (preparing html of a table): '+str(time.time()-dt)+' sec.<p>\n'

    if cmuoa=='':
        h+='</form>\n'

    # Add <br> to be able to select anchor on top
    for j in range(0,30):
        h+='<br>\n'

    return {'return':0, 'html':h, 'style':st}

##############################################################################
# show info for all layers

def html_viewer(i):
    """
    Input:  {
              data_uoa - CK entry UOA to view
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    duoa=i.get('data_uoa','')

    # Load entry
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    p=r['path']
    d=r['dict']

    dchars=d.get('characteristics',{})
    dchoices=d.get('choices',{})
    dmeta=d.get('meta',{})

    # Load stats
    dstat={}
    fstat=os.path.join(p,'ck-stat-flat-characteristics.json')
    if os.path.isfile(fstat):
        r=ck.load_json_file({'json_file':fstat, 'dict':dstat})
        if r['return']>0: return r
        dstat=r['dict']

    # Prepare table
    h=''
#    h+='<hr>\n'
    h+='<br>\n'
    h+='<center>\n'
    h+='<h2>DNN engine and model evaluation statistics per layer (crowd-tuning)</h2><br>\n'
    h+='</center>\n'

    xdeps=dmeta.get('xdeps',{})
    lcaffe=xdeps.get('lib-caffe',{})
    lmodel=xdeps.get('caffemodel',{})

    # Prepare extra info
    h+='<p>\n'
    h+='<table border="1" cellpadding="8" cellspacing="0">\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine name:</b></td>\n'
    h+='  <td>'+lcaffe.get('data_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine version:</b></td>\n'
    h+='  <td>'+lcaffe.get('ver','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine type:</b></td>\n'
    h+='  <td>'+dmeta.get('dnn_type','')+'</td>\n'
    h+=' </tr>\n'

    x=''

    dx=dmeta.get('xversions',{})
    for k in sorted(dx):
        v=dx[k]
        if v!='':
           if x!='': x+='<br>\n'
           x+=k+'='+str(v)+'\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine dependencies:</b></td>\n'
    h+='  <td>'+x+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN model name:</b></td>\n'
    h+='  <td>'+lmodel.get('data_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN model version:</b></td>\n'
    h+='  <td>'+lmodel.get('ver','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>Batch size:</b></td>\n'
    h+='  <td>'+dchars.get('run',{}).get('REAL_ENV_CK_CAFFE_BATCH_SIZE','')+'</td>\n'
    h+=' </tr>\n'

# TBD: Need to show min,exp,max!
#    h+=' <tr>\n'
#    h+='  <td><b>FWBW time (ms.):</b></td>\n'
#    h+='  <td>'+str(dchars.get('run',{}).get('time_bw_ms',''))+'</td>\n'
#    h+=' </tr>\n'

#    h+=' <tr>\n'
#    h+='  <td><b>FW time (ms.):</b></td>\n'
#    h+='  <td>'+str(dchars.get('run',{}).get('time_fw_ms',''))+'</td>\n'
#    h+=' </tr>\n'

#    h+=' <tr>\n'
#    h+='  <td><b>BW time (ms.):</b></td>\n'
#    h+='  <td>'+str(dchars.get('run',{}).get('time_bw_ms',''))+'</td>\n'
#    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>Platform:</b></td>\n'
    h+='  <td>'+dmeta.get('plat_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>OS:</b></td>\n'
    h+='  <td>'+dmeta.get('os_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>CPU:</b></td>\n'
    h+='  <td>'+dmeta.get('cpu_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>GPU:</b></td>\n'
    h+='  <td>'+dmeta.get('gpu_name','')+'</td>\n'
    h+=' </tr>\n'


    h+=' </tr>\n'
    h+='</table>\n'

    h+='<center>\n'
    h+='<p>\n'
    h+='<table border="0" cellpadding="10" cellspacing="0">\n'

    h+=' <tr>\n'
    h+='  <td><b>Name</b></td>\n'
    h+='  <td><b>Direction</b></td>\n'
    h+='  <td align="right"><b>Min time (ms.):</b></td>\n'
    h+='  <td align="right"><b>Expected time (ms.):</b></td>\n'
    h+='  <td align="right"><b>Max time (ms.):</b></td>\n'
    h+='  <td align="right"><b>Repetitions:</b></td>\n'
    h+=' </tr>\n'

    # Detecting number of layers
    jj={}

    for j in range(0,1000):
        k3='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#min'
        v3=dstat.get(k3,'')

        if v3=='': break

        jj[j]=v3

    # Sorting by min time
    if i.get('all_params',{}).get('skip_sort','')!='yes':
       jj=sorted(jj, key=lambda x: jj[x], reverse=True)

    # Also layers
    for j in jj:
        k1='##characteristics#run#per_layer_info@'+str(j)+'#direction#min'
        k2='##characteristics#run#per_layer_info@'+str(j)+'#label#min'
        k3='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#min'
        k4='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#max'
        k5='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#exp_allx'
        k7='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#repeats'

        v1=dstat.get(k1,'')
        v2=dstat.get(k2,'')
        v3=dstat.get(k3,'')
        v4=dstat.get(k4,'')
        v5=dstat.get(k5,[])
        v7=dstat.get(k7,'')

        if v1!='' and v2!='' and v3!='' and v4!='':
           v6=0
           if len(v5)>0:
              v6=v5[0]

           xv3=''
           xv4=''
           xv6=''

           if v3!='':
              if v3<0.1: xv3='0'
              else: xv3='<b>'+('%.1f'%v3)+'</b>'

           if v4!='':
              if v4<0.1: xv4='0'
              else: xv4='<b>'+('%.1f'%v4)+'</b>'

           if v6!='':
              if v6<0.1: xv6='0'
              else: xv6='<b>'+('%.1f'%v6)+'</b>'

           h+=' <tr>\n'
           h+='  <td>'+v2+'</td>\n'
           h+='  <td>'+v1+'</td>\n'
           h+='  <td align="right">'+xv3+'</td>\n'
           h+='  <td align="right">'+xv6+'</td>\n'
           h+='  <td align="right">'+xv4+'</td>\n'
           h+='  <td align="right">'+str(v7)+'</td>\n'
           h+=' </tr>\n'

    h+='</table>\n'

    h+='</center>\n'

    return {'return':0, 'html':h, 'show_top':'yes'}

##############################################################################
# replay experiment (TBD)

def replay(i):
    """
    Input:  {
              (data_uoa)
              (remote)

              (host_os)
              (target_os)
              (device_id)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    duoa=i.get('data_uoa','')
    remote=i.get('remote','')

    er=''
    esr=''

    if remote=='yes':
       er=i.get('exchange_repo','')
       if er=='': er=ck.cfg['default_exchange_repo_uoa']
       esr=i.get('exchange_subrepo','')
       if esr=='': esr=ck.cfg['default_exchange_subrepo_uoa']

    # Try to load info
    if o=='con':
       ck.out('Loading experiment entry ...')
       ck.out('')

    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa,
                 'repo_uoa':er,
                 'remote_repo_uoa':esr})
    if r['return']>0: return r

    d=r['dict']

    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # Check two main deps (engine and model)
    meta=d.get('meta',{})
    xdeps=meta.get('xdeps',{})

#    TBD: rebuild env by tags!
#
#    dnn=xdeps.get('lib-caffe',{})
#    model=xdeps.get('caffemodel',{})
#
#    pdnn=dnn.get('package_uoa','')
#    pmodel=model.get('package_uoa','')
#
#    preset_env={}
#    penv=[pdnn,pmodel]
#
#    for j in range(0, len(penv)):
#        px=''
#        py=penv[j]
#
#        if py!='':
#           # Search by package
#           r=ck.access({'action':'search',
#                        'module_uoa':cfg['module_deps']['env'],
#                        'search_dict':{'package_uoa':py}})
#           if r['return']>0: return r
#
#           l=r['lst']
#
#        if j==0: preset_env['lib-caffe']=px
#        elif j==1: preset_env['caffemodel']=px

    # Run pipeline
    choices=d.get('choices',{})
    
    # Clean various vars
    for k in replay_clean_vars:
        if k in choices:
           del(choices[k])

    if i.get('target_os','')!='' and not i['target_os'].startswith('android'):
       del(i['target_os'])

    env=choices.get('env',{})
    for k in replay_clean_env_vars:
        if k in env:
           del(env[k])
    choices['env']=env

    if hos!='': choices['host_os']=hos
    if tos!='': choices['target_os']=tos
    if tdid!='': choices['device_id']=tdid

    pipeline_data_uoa=choices['module_uoa']

    # Prepare pipeline
    ii={'action':'pipeline',
        'module_uoa':cfg['module_deps']['program'],
        'prepare':'yes',
        'choices':choices,
        'out':o}
    rr=ck.access(ii)
    if rr['return']>0: return rr

    fail=rr.get('fail','')
    if fail=='yes':
        return {'return':10, 'error':'pipeline failed ('+rr.get('fail_reason','')+')'}

    ready=rr.get('ready','')
    if ready!='yes':
        return {'return':11, 'error':'couldn\'t prepare universal CK program workflow'}

    # Run pipeline
    ii={'action':'run',
        'module_uoa':cfg['module_deps']['pipeline'],
        'data_uoa':pipeline_data_uoa,
        'pipeline':rr,
        'out':o}
    rr=ck.access(ii)
    if rr['return']>0: return rr

    fail=rr.get('fail','')
    if fail=='yes':
        return {'return':10, 'error':'pipeline failed ('+rr.get('fail_reason','')+')'}

    if o=='con':
       ck.out('')
       ck.out('Your results:')
       ck.out('')

       dstat=rr.get('last_stat_analysis',{}).get('dict_flat',{})

       x0=dstat.get("##characteristics#run#time_fwbw_ms#min",None)
       x0e=dstat.get("##characteristics#run#time_fwbw_ms#exp",None)

       if x0!=None:
            ck.out('* FWBW min: '+('%.0f'%x0)+' ms.')
       if x0e!=None:
            ck.out('* FWBW exp: '+('%.0f'%x0e)+' ms.')

       x1=dstat.get("##characteristics#run#time_fw_ms#min",None)
       x1e=dstat.get("##characteristics#run#time_fw_ms#exp",None)

       if x1!=None:
            ck.out('* FW   min: '+('%.0f'%x1)+' ms.')
       if x1e!=None:
            ck.out('* FW   exp: '+('%.0f'%x1e)+' ms.')

       x2=dstat.get("##characteristics#run#time_bw_ms#min",None)
       x2e=dstat.get("##characteristics#run#time_bw_ms#exp",None)

       if x2!=None:
            ck.out('* BW   min: '+('%.0f'%x2)+' ms.')
       if x2e!=None:
            ck.out('* BW   exp: '+('%.0f'%x2e)+' ms.')

    return {'return':0}

##############################################################################
# see ReQuEST results (CK Dashboard)

def dashboard(i):
    """
    Input:  {
              (host)        - Internal web server host
              (port)        - Internal web server port

              (wfe_host)    - External web server host
              (wfe_port)    - External web server port

              (extra_url)   - extra URL
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

#    Old style
#    i['action']='browser'
#    i['cid']=''
#    i['module_uoa']=''
#    i['template']='nntest'


    i['action']='start'
    i['module_uoa']='web'
    i['browser']='yes'
    i['template']='request.asplos18'
    i['cid']=''

    return ck.access(i)

##############################################################################
# prepare common meta for ReQuEST @ ASPLOS"18

def prepare_common_meta(i):
    """
    Input:  {
              platform_dict - output from platform detection
              request_dict  - info about ReQuEST submission
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              tags        - tags for experiment entry
              meta        - meta for experiment entry
              record_dict - dict to update records
            }

    """

    from time import strftime, gmtime
    import copy

    # Get current timestamp
    r=ck.get_current_date_time({})
    if r['return']>0: return r
    timestamp=r['iso_datetime']

    #striped timestamp
    j=timestamp.find('.')
    if j>0: timestamp=timestamp[:j]

    stimestamp=timestamp.replace('-','').replace(':','').replace('T','')

    pd=i['platform_dict']
    rd=i['request_dict']

    tags=[
      'request',
      'request-asplos18',
      timestamp,
      stimestamp
    ]

    meta=copy.deepcopy(rd)

    tags.append(meta['algorithm_species'])

    rd={
         'subview_uoa':'f84ca49f79a1446a'  # ReQuEST default table view from ck-autotuning repo
                                           # ck-autotuning:experiment.view:request-default
       }




    return {'return':0, 'tags':tags, 'meta':meta, 'record_dict':rd}
